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

# def postArticle(page):
#     # Write article content

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

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
    page.wait_for_selector("[data-test=\"menuItem-pages\"]")
    page.locator("[data-test=\"menuItem-pages\"]").click()
    # This next step doesn't work as the yui id changes UP TO HERE
    page.locator("#yui_3_17_2_1_1724891609340_23559").click()
    page.locator("[data-test=\"blog-add-item\"]").click()

    page.get_by_placeholder("Enter a post title…").fill(data['article']['title'])
    page.get_by_label("Text").get_by_role("paragraph").fill(data['article']['body'])

    if data['article']['disclaimers']:
        for disclaimer in data['article']['disclaimers']:
            page.get_by_label("Text").get_by_role("paragraph").type('\n\n') 
            page.get_by_label("Text").get_by_role("paragraph").type(disclaimer)

    page.locator("[data-test=\"dialog-saveAndPublish\"]").click()

    context.close()
    browser.close()
    playwright.stop()



with sync_playwright() as playwright:
    run(playwright)
