# step-by-step run command: PWDEBUG=1 pytest -s PostFacebookArticle.py IN GIT BASH TERMINAL


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

def format_hashtag(tag: str) -> str:
    return f'#{tag.replace(" ", "").lower()}'

def postArticle(page):
    page.get_by_role("button", name="What's on your mind?").click()
    page.get_by_label("What's on your mind?").type(f"{data['article']['intro']}\n\n")

    # Add hashtags
    for tag in data['article']['tags']:
        formatted_tag = format_hashtag(tag)
        page.get_by_label("What's on your mind?").type(formatted_tag + ' ')

    page.get_by_label("What's on your mind?").type(f"\n\n{data['article']['linkedin_post_link']}")

    page.pause()
    page.get_by_label("Post", exact=True).click()


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
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # auth_state_path = os.path.join(current_dir, '..', 'playwright', '.auth', 'facebookAuthState.json')

    print("Could not find existing auth state from facebookAuthState.json")
    facebookUsername = os.getenv("FACEBOOK_USERNAME")
    facebookPassword = os.getenv("FACEBOOK_PASSWORD")

    if not facebookUsername or not facebookPassword:
        print("Error: Missing Facebook Credentials! Please ensure both 'facebookUsername' and 'facebookPassword' environment variables are set in your '.env' file.")
        return
    
    # Login to Facebook
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.facebook.com/people/Dion-Guagliardo/100067720235998/")
    page.get_by_role("textbox", name="Email address or phone number").fill(facebookUsername)
    page.locator("#login_popup_cta_form").get_by_role("textbox", name="Password").fill(facebookPassword)
    page.get_by_label("Accessible login button").click()
    page.pause()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Trust this device").click()
    page.get_by_role("button", name="Your profile", exact=True).click()
    page.get_by_label("Switch to Dion Guagliardo").click()
    
    # # Save storage state for future use
    # context.storage_state(path=auth_state_path)
    # print("Saved storage state to facebookAuthState.json")

        # Post an article
    postArticle(page)
    
    #savePostURL(data, postUrl)
    #repostOnFortress(page, postUrl)
    

    page.pause()


with sync_playwright() as playwright:
    run(playwright)
