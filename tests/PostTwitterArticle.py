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

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    twitterUsername = os.getenv("TWITTER_USERNAME")
    twitterPassword = os.getenv("TWITTER_PASSWORD")
    if not twitterUsername or not twitterPassword:
        print("Error: Missing Twitter Credentials! Please ensure both 'twitterUsername' and 'twitterPassword' environment variables are set in your '.env' file.")
        return
    
    # Login to LinkedIn
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://x.com/i/flow/login")
    page.get_by_label("Phone, email address, or").fill(twitterUsername)
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Password", exact=True).fill(twitterPassword)
    page.get_by_test_id("LoginForm_Login_Button").click()
    page.get_by_test_id("tweetTextarea_0").fill(data['article']['twitter_post'])
    page.get_by_test_id("tweetButtonInline").hover()
    page.wait_for_timeout(5000) 


    # postLink = postArticle(page)
    # repostOnFortress(page, "https://www.linkedin.com/posts/dion-guagliardo_inflation-interestrates-rba-activity-7204366788891959298-fzs1?utm_source=share&utm_medium=member_desktop")

    # ---------------------
    context.close()



with sync_playwright() as playwright:
    run(playwright)
