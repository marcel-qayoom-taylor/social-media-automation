# step-by-step run command: PWDEBUG=1 pytest -s PostLinkedinArticle.py IN GIT BASH TERMINAL


import re
import os
import asyncio
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import json

load_dotenv()  # Loads variables from the .env file


# Read input data
with open('../data.json', 'r') as f:
    data = json.load(f)

def postArticle(page):
    # Write article content
    page.get_by_label("Write an article on LinkedIn").click()
    page.get_by_role("radio", name="Dion Guagliardo").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_placeholder("Title").press_sequentially(data['article']['title'])
    
    expect(page).to_have_url(re.compile(".*article/edit/")) # Wait for editor to save (have article/edit in url)
    page.get_by_label("Article editor content").fill(data['article']['body'])

    # TO DO: Disclaimers

    # Add image
    page.get_by_label("Upload from computer").set_input_files(data['article']['image_path']) # image has to be in directory or use file picker but needs async
    
    # Move to publish page
    page.get_by_role("button", name="Next").click(delay=2000) # wait for draft to save
    page.get_by_label("Text editor for creating").press_sequentially(data['article']['intro']) # this not working but i need spacing
    page.get_by_label("Text editor for creating").press_sequentially('\n\n') 

    # Add hashtags
    for tag in data['article']['tags']:
        hashtag = '#' + str(tag) + ' '
        page.get_by_label("Text editor for creating").press_sequentially(hashtag)

    # page.get_by_label("Publish").click()
    # return page.url()

def repostOnFortress(page, postLink):
    page.goto(postLink)
    page.get_by_role("button", name="Repost", exact=True).click()
    page.get_by_role("button", name="Repost with your thoughts").click()
    page.get_by_role("button", name="Dion Guagliardo Dion").click()
    page.get_by_role("button", name="Dion Guagliardo").click()
    page.get_by_role("radio", name="Fortress Family Office").click()
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Done").click()
    page.get_by_role("button", name="Post").click()

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    try: 
        context = browser.new_context(storage_state="..\playwright\.auth\linkedinAuthState.json")
        
        # Open linkedin using saved credentials
        page = context.new_page()
        page.goto("https://www.linkedin.com/feed/")
        print("Loaded existing storage state from linkedinAuthState.json")
    except FileNotFoundError: # if no credentials cached
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
        context.storage_state(path="..\playwright\.auth\linkedinAuthState.json")
        print("Saved storage state to state.json")

    # Post an article
    #postArticle(page)

    # postLink = postArticle(page)
    repostOnFortress(page, "https://www.linkedin.com/posts/dion-guagliardo_inflation-interestrates-rba-activity-7204366788891959298-fzs1?utm_source=share&utm_medium=member_desktop")

    # ---------------------
    context.close()
    browser.close()
    playwright.stop()


with sync_playwright() as playwright:
    run(playwright)
