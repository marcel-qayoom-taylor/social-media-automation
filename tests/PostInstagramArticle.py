# step-by-step run command: PWDEBUG=1 pytest -s PostInstagramArticle.py IN GIT BASH TERMINAL

import os
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import json
# from ..utils import format_hashtag

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
    page.get_by_label("Write a caption...").fill(data['article']['title'])
    page.get_by_label("Write a caption...").type('\n\n')  # Simulate pressing Enter
    page.get_by_label("Write a caption...").type(data['article']['intro'])
    page.get_by_label("Write a caption...").type('\n\n')  # Simulate pressing Enter
    page.get_by_label("Write a caption...").type('Link to full article in bio 🔗')
    page.get_by_label("Write a caption...").type('\n\n')  # Simulate pressing Enter

    for tag in data['article']['tags']:
        formatted_tag = format_hashtag(tag)
        page.get_by_label("Write a caption...").type(formatted_tag + ' ')
    
    if os.getenv("MODE") == "PROD":
        page.get_by_role("button", name="Share").click()
    else:
        print("Post successfully created. Skipping publish step.")
        page.wait_for_timeout(3000)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    
    # # Get the absolute path for the auth state file
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # auth_state_path = os.path.join(current_dir, '..', 'playwright', '.auth', 'instagramAuthState.json')
    # print('auth path is ' + auth_state_path)

    # try: 
    #     # Open Instagram using saved credentials
    #     context = browser.new_context(storage_state=auth_state_path)
    #     page = context.new_page()
    #     page.goto("https://www.instagram.com")
    #     print("Loaded existing storage state from instagramAuthState.json")
    # except FileNotFoundError:
    print("Could not find existing auth state from instagramAuthState.json")
    instagramUsername = os.getenv("INSTAGRAM_USERNAME")
    instagramPassword = os.getenv("INSTAGRAM_PASSWORD")

    if not instagramUsername or not instagramPassword:
        print("Error: Missing instagram Credentials! Please ensure both 'instagramUsername' and 'instagramPassword' environment variables are set in your '.env' file.")
        return

    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.instagram.com/accounts/login")
    page.get_by_label("Phone number, username or email address").fill(instagramUsername)
    page.get_by_label("Password").fill(instagramPassword)
    page.get_by_role("button", name="Log in", exact=True).click()

    # Post an article
    postArticle(page)

    # ---------------------
    context.close()
    browser.close()
    playwright.stop()

with sync_playwright() as playwright:
    run(playwright)
