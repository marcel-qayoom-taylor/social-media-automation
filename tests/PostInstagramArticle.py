# step-by-step run command: PWDEBUG=1 pytest -s PostInstagramArticle.py IN GIT BASH TERMINAL


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
    instagramUsername = os.getenv("INSTAGRAM_USERNAME")
    instagramPassword = os.getenv("INSTAGRAM_PASSWORD")
    
    if not instagramUsername or not instagramPassword:
        print("Error: Missing instagram Credentials! Please ensure both 'instagramUsername' and 'instagramPassword' environment variables are set in your '.env' file.")
        return

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.instagram.com/accounts/login")
    page.get_by_label("Phone number, username or email address").fill(instagramUsername)
    page.get_by_label("Password").fill(instagramPassword)
    page.get_by_role("button", name="Log in", exact=True).click()
    page.get_by_role("link", name="New post Create").click()
    page.get_by_role("link", name="Post Post").click()

    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Select from computer").click()
    file_chooser = fc_info.value
    file_chooser.set_files(data['article']['image_path'])

    page.locator("button").filter(has_text="Select crop").click()
    page.get_by_role("button", name="Original Photo outline icon").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("paragraph").click()

    # Fill in the title, intro, hashtags, link in bio
    # FIX: .FILL OVERWRITERS TEXT
    page.get_by_label("Write a caption...").fill(data['article']['title'])
    page.get_by_label("Write a caption...").fill('\n\n')
    page.get_by_label("Write a caption...").fill(data['article']['intro'])
    page.get_by_label("Write a caption...").fill('\n\n')
    page.get_by_label("Write a caption...").fill('Link to full article in bio 🔗')
    page.get_by_label("Write a caption...").fill('\n\n')

    # FIX: MAKE HASHTAGS LOWERCASE AND REMOVE SPACE
    for tag in data['article']['tags']:
        hashtag = '#' + str(tag) + ' '
        page.get_by_label("Write a caption...").fill(hashtag)
    
    if os.getenv("MODE") == "PROD":
        page.get_by_role("button", name="Share").click()
    else:
        print("Post successfully created. Skipping publish step.")
        page.wait_for_timeout(3000)

    # Post an article
    # postArticle(page)

    # postLink = postArticle(page)
    # repostOnFortress(page, "https://www.instagram.com/posts/dion-guagliardo_inflation-interestrates-rba-activity-7204366788891959298-fzs1?utm_source=share&utm_medium=member_desktop")

    # ---------------------
    #context.close()



with sync_playwright() as playwright:
    run(playwright)
