# step-by-step run command: PWDEBUG=1 pytest -s PostMediumArticle.py IN GIT BASH TERMINAL


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

# def postArticle(page):
#     # Write article content

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    # Get the absolute path for the auth state file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    auth_state_path = os.path.join(current_dir, '..', 'playwright', '.auth', 'squarespaceAuthState.json')

    try: 
        context = browser.new_context(storage_state=auth_state_path)
        
        # Open medium using saved credentials
        page = context.new_page()
        page.goto("https://medium.com/new-story")
        print("Loaded existing storage state from mediumAuthState.json")
    except FileNotFoundError: # if no credentials cached
        print("Could not find existing auth state from mediumAuthState.json")
        mediumUsername = os.getenv("MEDIUM_USERNAME")
        mediumPassword = os.getenv("MEDIUM_PASSWORD")
        if not mediumUsername or not mediumPassword:
            print("Error: Missing Medium Credentials! Please ensure both 'mediumUsername' and 'mediumPassword' environment variables are set in your '.env' file.")
            return
        
        # Login to LinkedIn
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://medium.com/m/signin")
        page.get_by_role("link", name="Sign in with Google").click()
        page.get_by_label("Email or phone").fill("fortressfinancialmedia@gmail.com")
        page.get_by_role("button", name="Next").click()

    
    page.pause()



with sync_playwright() as playwright:
    run(playwright)
