# step-by-step run command: PWDEBUG=1 pytest -s PostLinkedinArticle.py IN GIT BASH TERMINAL


import re
import os
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import json

load_dotenv()  # Loads variables from the .env file


# Read input data
with open('../postData.json', 'r') as f:
    data = json.load(f)

# def postArticle(page):
#     # Write article content


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    try: 
        context = browser.new_context(storage_state="..\playwright\.auth\mediumAuthState.json")
        
        # Open medium using saved credentials
        page = context.new_page()
        page.goto("https://medium.com/")
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

    
    #browser.close()
    #playwright.stop()
    # try: 
    #     context = browser.new_context(storage_state="..\playwright\.auth\mediumAuthState.json")
        
    #     # Open linkedin using saved credentials
    #     page = context.new_page()
    #     page.goto("https://medium.com/new-story")
    #     print("Loaded existing storage state from mediumAuthState.json")
    # except FileNotFoundError: # if no credentials cached
    #     print("Could not find existing auth state from mediumAuthState.json")
    #     linkedinUsername = os.getenv("MEDIUM_USERNAME")
    #     linkedinPassword = os.getenv("MEDIUM_PASSWORD")
    #     if not linkedinUsername or not linkedinPassword:
    #         print("Error: Missing Medium Credentials! Please ensure both 'mediumUsername' and 'mediumPassword' environment variables are set in your '.env' file.")
    #         return
        
    #     # Login to LinkedIn
    #     context = browser.new_context()
    #     page = context.new_page()
    #     page.goto("https://medium.com/m/signin")
    #     page.get_by_label("Sign in with email").press_sequentially(linkedinUsername)
    #     page.get_by_label("Password", exact=True).press_sequentially(linkedinPassword)
    #     page.get_by_label("Sign in", exact=True).click()
        
    #     # Save storage state for future use
    #     context.storage_state(path="..\playwright\.auth\linkedinAuthState.json")
    #     print("Saved storage state to state.json")

    # Post an article
    # postArticle(page)

    # postLink = postArticle(page)
    # repostOnFortress(page, "https://www.linkedin.com/posts/dion-guagliardo_inflation-interestrates-rba-activity-7204366788891959298-fzs1?utm_source=share&utm_medium=member_desktop")

    # ---------------------
    #context.close()



with sync_playwright() as playwright:
    run(playwright)
