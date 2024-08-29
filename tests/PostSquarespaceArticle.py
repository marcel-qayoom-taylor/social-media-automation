# step-by-step run command: PWDEBUG=1 pytest -s PostSquarespaceArticle.py IN GIT BASH TERMINAL


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
    page.wait_for_selector("[data-test=\"menuItem-pages\"]")
    page.locator("[data-test=\"menuItem-pages\"]").click()
    page.locator('[title="Insights"]').nth(1).click();
    page.locator("[data-test=\"blog-add-item\"]").click()

    page.get_by_placeholder("Enter a post title…").fill(data['article']['title'])
    
    bodyContent = data['article']['body']

    for disclaimer in data['article']['disclaimers']:
        bodyContent += "\n\n"
        bodyContent += f"\n{disclaimer}"

    page.get_by_label("Text").get_by_role("paragraph").fill(bodyContent)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    # Get the absolute path for the auth state file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    auth_state_path = os.path.join(current_dir, '..', 'playwright', '.auth', 'squarespaceAuthState.json')

    try: 
        # Open Squarespace using saved credentials

        context = browser.new_context(storage_state=auth_state_path)        
        page = context.new_page()
        page.goto("https://fortressfamilyoffice.squarespace.com/config/")
        print("Loaded existing storage state from squarespaceAuthState.json")
    except FileNotFoundError:
        print("Could not find existing auth state from squarespaceAuthState.json")
        squarespaceUsername = os.getenv("SQUARESPACE_USERNAME")
        squarespacePassword = os.getenv("SQUARESPACE_PASSWORD")

        if not squarespaceUsername or not squarespacePassword:
            print("Error: Missing Squarespace Credentials! Please ensure both 'instagramUsername' and 'instagramPassword' environment variables are set in your '.env' file.")
            return
    
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://login.squarespace.com/")
        page.get_by_placeholder("name@example.com").fill(squarespaceUsername)
        page.get_by_placeholder("Password").fill(squarespacePassword)
        page.locator("[data-test=\"login-button\"]").click()
        page.get_by_role("link", name="Fortress Family Office").click()

        # Save storage state for future use
        context.storage_state(path=auth_state_path)
        print("Saved storage state to linkedinAuthState.json")


    postArticle(page)

    page.pause()





with sync_playwright() as playwright:
    run(playwright)
