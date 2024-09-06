# DONE
# step-by-step run command: PWDEBUG=1 pytest -s PostMailchimpArticle.py IN GIT BASH TERMINAL

import os
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import json
from datetime import datetime


load_dotenv()  # Loads variables from the .env file

# Read input data
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, '../postData.json')

with open(json_path, 'r') as f:
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Cannot find the file: {json_path}")
    data = json.load(f)

def postArticle(page):
    page.goto("https://admin.mailchimp.com/templates/")
    page.locator("li").filter(has_text="Weekly Article").get_by_test_id("combobutton-expand-button").click()
    page.get_by_role("link", name="Create Email").click()

    page.get_by_role("button", name="Edit name").click()
    # Get today's date in DD/MM/YYYY format
    today_date = datetime.now().strftime("%d/%m/%Y")
    page.get_by_placeholder("Name your email").fill(f"Weekly Insights {today_date}")
    page.get_by_role("button", name="Save").click()

    page.get_by_role("button", name="Add subject").click()
    page.get_by_label("Subject").fill(f"Weekly Insights: {data['article']['title']}")

    page.get_by_label("Preview Text").fill(data['article']['body'][:147] + "...")
    page.get_by_role("button", name="Save").click()

    page.get_by_role("button", name="Add send time").click()
    page.locator("label").filter(has_text="Send now").click()
    page.get_by_role("button", name="Save").click()

    page.get_by_role("button", name="Edit design").click()
    page.frame_locator("iframe[title=\"Preview\"]").locator("#dataBlockId-5").get_by_role("paragraph").first.click()
    page.frame_locator("iframe[title=\"Preview\"]").locator("#dataBlockId-5").get_by_role("paragraph").first.fill(data['article']['title'] + '\n\n' + data['article']['body'])
    page.frame_locator("iframe[title=\"Preview\"]").locator("#dataBlockId-5").get_by_role("paragraph").first.click(click_count=3)
    page.get_by_role("button", name="Set bold style on text").click()

    page.pause()

    page.get_by_role("button", name="Save and exit").click()
    page.get_by_role("button", name="Send a Test Email").click()
    page.get_by_role("button", name="Send test").click()
    page.get_by_role("button", name="Ok", exact=True).click()

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    # Get the absolute path for the auth state file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    auth_state_path = os.path.join(current_dir, '..', 'playwright', '.auth', 'mailchimpAuthState.json')

    try: 
        # Open Mailchimp using saved credentials
        context = browser.new_context(storage_state=auth_state_path)        
        page = context.new_page()
        page.goto("https://admin.mailchimp.com/campaigns/")
        expect(page.get_by_test_id("LeftNavigation").get_by_role("link", name="Create")).to_be_visible()
        print("Loaded existing storage state from mailchimpAuthState.json")
    except:
        print("Could not find existing auth state from mailchimpAuthState.json OR something went wrong")
        mailchimpUsername = os.getenv("MAILCHIMP_USERNAME")
        mailchimpPassword = os.getenv("MAILCHIMP_PASSWORD")

        if not mailchimpUsername or not mailchimpPassword:
            print("Error: Missing Mailchimp Credentials! Please ensure both 'mailchimpUsername' and 'mailchimpPassword' environment variables are set in your '.env' file.")
            return
    
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://login.mailchimp.com/")
        page.get_by_label("Username or Email").fill(mailchimpUsername)
        page.get_by_label("Password").fill(mailchimpPassword)
        page.get_by_role("button", name="Log in").click()
        page.pause()

        # Save storage state for future use
        context.storage_state(path=auth_state_path)
        print("Saved storage state to mailchimpAuthState.json")


    postArticle(page)

    page.pause()





with sync_playwright() as playwright:
    run(playwright)
