# step-by-step run command: PWDEBUG=1 pytest -s PostLinkedinArticle.py IN GIT BASH TERMINAL


import re
import os
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import json

load_dotenv()  # Loads variables from the .env file

# Read input data
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, '../postData.json')

with open(json_path, 'r') as f:
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Cannot find the file: {json_path}")
    data = json.load(f)

def postArticle(page):
    # Write article content
    page.get_by_label("Write an article on LinkedIn").click()
    page.get_by_placeholder("Title").press_sequentially(data['article']['title'])
    
    expect(page).to_have_url(re.compile(".*article/edit/")) # Wait for editor to save (have article/edit in url)
    page.get_by_label("Article editor content").fill(data['article']['body'])

    # NEED TO ADD DISCLAIMERS

    # Add image
    with page.expect_file_chooser() as fc_info:
        page.get_by_label("Upload from computer").click()
    file_chooser = fc_info.value
    file_chooser.set_files(data['article']['image_path']) 
    page.get_by_label("Next").click(delay=2000)

    # Move to publish page
    page.get_by_role("button", name="Next").click(delay=2000) # wait for draft to save
    page.get_by_label("Text editor for creating").fill(data['article']['intro']) # this not working but i need spacing
    page.get_by_label("Text editor for creating").fill('\n\n') 

    # Add hashtags
    for tag in data['article']['tags']:
        hashtag = '#' + str(tag) + ' '
        page.get_by_label("Text editor for creating").fill(hashtag)

    if os.getenv("MODE") == "PROD":
        page.get_by_label("Publish").click()
        return page.url()
    else:
        print("Article successfully created. Skipping publish step.")
        page.wait_for_timeout(3000) 
        return page.url()

def repostOnFortress(page, postLink):
    page.goto(postLink)
    page.get_by_role("button", name="Repost", exact=True).click()
    page.get_by_role("button", name="Repost with your thoughts").click()
    page.get_by_role("button", name="Dion Guagliardo Dion").click()
    page.get_by_role("button", name="Dion Guagliardo").click()
    page.get_by_role("radio", name="Fortress Family Office").click()
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Done").click()
    if os.getenv("MODE") == "PROD":
        page.get_by_role("button", name="Post").click()
    else:
        print("Repost successfully near-complete. Skipping publish step.")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    
    # Get the absolute path for the auth state file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    auth_state_path = os.path.join(current_dir, '..', 'playwright', '.auth', 'linkedinAuthState.json')
    
    try: 
        # Open LinkedIn using saved credentials

        context = browser.new_context(storage_state=auth_state_path)        
        page = context.new_page()
        page.goto("https://www.linkedin.com/feed/")
        print("Loaded existing storage state from linkedinAuthState.json")
    except FileNotFoundError:
        print("Could not find existing auth state from linkedinAuthState.json")
        linkedinUsername = os.getenv("LINKEDIN_USERNAME")
        linkedinPassword = os.getenv("LINKEDIN_PASSWORD")
        
        if not linkedinUsername or not linkedinPassword:
            print("Error: Missing LinkedIn Credentials! Please ensure both 'linkedinUsername' and 'linkedinPassword' environment variables are set in your '.env' file.")
            return
        
        # Login to LinkedIn
        context = browser.new_context()
        
        page = context.new_page()
        page.goto("https://www.linkedin.com/login")
        page.get_by_label("Email or phone").press_sequentially(linkedinUsername)
        page.get_by_label("Password", exact=True).press_sequentially(linkedinPassword)
        page.get_by_label("Sign in", exact=True).click()
        
        # Save storage state for future use
        context.storage_state(path=auth_state_path)
        print("Saved storage state to linkedinAuthState.json")

    # Post an article
    
    postArticle(page)
    #postLink = postArticle(page)
    #repostOnFortress(page, postLink)


    # postLink = postArticle(page)
    # repostOnFortress(page, "https://www.linkedin.com/posts/dion-guagliardo_inflation-interestrates-rba-activity-7204366788891959298-fzs1?utm_source=share&utm_medium=member_desktop")

    # ---------------------
    context.close()
    browser.close()
    playwright.stop()


with sync_playwright() as playwright:
    run(playwright)
