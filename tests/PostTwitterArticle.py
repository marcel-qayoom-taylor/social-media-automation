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

def postTweet(browser, postContent):
    context = browser.new_context()

    twitterUsername = os.getenv("TWITTER_USERNAME")
    twitterPassword = os.getenv("TWITTER_PASSWORD")
    if not twitterUsername or not twitterPassword:
        print("Error: Missing Twitter Credentials! Please ensure both 'twitterUsername' and 'twitterPassword' environment variables are set in your '.env' file.")
        return
    
    # Login to Twitter
    
    page = context.new_page()
    page.goto("https://x.com/i/flow/login")
    page.get_by_label("Phone, email address, or").fill(twitterUsername)
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Password", exact=True).fill(twitterPassword)
    page.get_by_test_id("LoginForm_Login_Button").click()

    # Post tweet
    page.get_by_test_id("tweetTextarea_0").type(postContent)

    if os.getenv("MODE") == "PROD":
        page.get_by_test_id("tweetButtonInline").click()
    else:
        print("Twitter post successfully created. Skipping publish step due to being in dev mode")
        page.pause()

def retweet(browser, postLink):
    context = browser.new_context()
    
    repostAccountUsername = os.getenv("FORTRESS_TWITTER_USERNAME")
    repostAccountPassword = os.getenv("FORTRESS_TWITTER_PASSWORD")
    if not repostAccountUsername or not repostAccountPassword:
        print("Error: Missing Twitter Credentials! Please ensure both 'twitterUsername' and 'twitterPassword' environment variables are set in your '.env' file.")
        return
    
    # Login to Twitter
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://x.com/i/flow/login")
    page.get_by_label("Phone, email address, or").fill(repostAccountUsername)
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Password", exact=True).fill(repostAccountPassword)
    page.get_by_test_id("LoginForm_Login_Button").click()

    page.goto(postLink)
    page.get_by_role("button", name="Retweet", exact=True).click()

    page.locator('button[data-testid="retweet"]:first-of-type').click()
    
    if os.getenv("MODE") == "PROD":
        page.get_by_test_id("retweetConfirm").click()
    else:
        page.pause()


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    postContent = ""

    if data['article']['linkedin_article_link']:
        postContent = data['article']['twitter_post'] + '\n\n' + data['article']['linkedin_article_link']
    else:
        postContent = data['article']['twitter_post']
    
    postTweet(browser, postContent)

    # retweet(browser, "https://twitter.com/fortress_fo/status/1440730730730730730")

with sync_playwright() as playwright:
    run(playwright)
