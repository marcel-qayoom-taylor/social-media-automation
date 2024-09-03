# DONE
# step-by-step run command: PWDEBUG=1 pytest -s PostMailchimpArticle.py IN GIT BASH TERMINAL


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
    auth_state_path = os.path.join(current_dir, '..', 'playwright', '.auth', 'mailchimpAuthState.json')

    try: 
        # Open Mailchimp using saved credentials

        context = browser.new_context(storage_state=auth_state_path)        
        page = context.new_page()
        page.goto("https://admin.mailchimp.com/campaigns/")
        print("Loaded existing storage state from mailchimpAuthState.json")
    except FileNotFoundError:
        print("Could not find existing auth state from mailchimpAuthState.json")
        mailchimpUsername = os.getenv("MAILCHIMP_USERNAME")
        mailchimpPassword = os.getenv("MAILCHIMP_PASSWORD")

        if not mailchimpUsername or not mailchimpPassword:
            print("Error: Missing Mailchimp Credentials! Please ensure both 'instagramUsername' and 'instagramPassword' environment variables are set in your '.env' file.")
            return
    
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://login.mailchimp.com/")

        # RAW CODE

    page.get_by_label("Username or Email").click()
    page.get_by_label("Username or Email").fill("t")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("t")
    page.get_by_role("button", name="Log in").click()
    page.get_by_label("Username or Email").click()
    page.get_by_label("Username or Email").fill("admin@fortressfamilyoffice.com")
    page.get_by_label("Password").fill("Jimbo1953#")
    page.get_by_label("Password").click()
    page.get_by_role("button", name="Log in").click()
    page.get_by_role("button", name="Send SMS code").click()
    page.get_by_label("Send code via email").check()
    page.get_by_role("button", name="Send email code").click()
    page.get_by_placeholder("Enter email code").click()
    page.get_by_placeholder("Enter email code").fill("535078")
    page.get_by_role("button", name="Submit verification").click()
    page.get_by_test_id("LeftNavigation").get_by_role("link", name="Campaigns").click()
    page.get_by_label("All campaigns").click()
    page.get_by_role("row", name="Bulk select Weekly Insights 29/08/24 Weekly Insights 29/08/24 Regular email").get_by_role("button").click()
    page.get_by_test_id("replicate-dropdown-action").click()
    page.get_by_role("button", name="Edit name").click()
    page.get_by_placeholder("Name your email").click()
    page.get_by_placeholder("Name your email").click()
    page.get_by_placeholder("Name your email").fill("Weekly Insights 03/09/2024")
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Edit subject").click()
    page.get_by_label("Subject").click(click_count=3)
    page.get_by_label("Subject").fill("Weekly Insights: ")
    page.get_by_label("Subject").click()
    page.get_by_label("Subject").fill("Weekly Insights: Debts and Deficits ")
    page.get_by_label("Preview Text").click(click_count=3)
    page.get_by_label("Preview Text").fill("Investors are trying to work out just what a win for either Trump or Harris means for their investments, the economy and the ramifications for the entire world. ")
    page.get_by_label("Preview Text").click(modifiers=["Shift"])
    page.get_by_label("Preview Text").press("ArrowRight")
    page.get_by_label("Preview Text").press("ArrowLeft")
    page.get_by_label("Preview Text").press("ArrowLeft")
    page.get_by_label("Preview Text").press("ArrowLeft")
    page.get_by_label("Preview Text").press("ControlOrMeta+ArrowLeft")
    page.get_by_label("Preview Text").fill("Investors are trying to work out just what a win for either Trump or Harris means for their investments, the economy and the ramifications for the world. ")
    page.get_by_label("Preview Text").press("ControlOrMeta+ArrowLeft")
    page.get_by_label("Preview Text").fill("Investors are trying to work out just what a win for either Trump or Harris means for their investments, the economy and the world. ")
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Add send time").click()
    page.locator("label").filter(has_text="Send nowGet your email out").click()
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Edit design").click()
    page.locator("div:nth-child(3) > div > img").click()
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had?", exact=True).click()
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had?", exact=True).click()
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+ArrowRight")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+ArrowRight")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+ArrowRight")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+ArrowRight")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+ArrowRight")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+Shift+ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+Shift+ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+Shift+ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+Shift+ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+Shift+ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+Shift+ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").press("ControlOrMeta+Shift+ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Are You The Leader You Wish You Had? One of my favourite parts of interviewing").fill(" \n\n\n\n\nOne of my favourite parts of interviewing exceptional leaders and businesspeople on my podcast is hearing the stories that are unique to their journeys. While high performers have many similar traits, there are always insights to uncover based on each person's path and hard-earned lessons along the way.  \n\n\n\n\nWith that in mind, I was especially looking forward to speaking with Sydney Swans Premiership coach and AFL Legend Paul Roos on my most recent episode. There were so many awesome insights across a range of topics. We covered everything from success and failure to culture and leading through to mentoring, succession, family, and parenting. \n\n\n\n\nWhen he retired as a player in 1998, he compiled a list of 25 'Coaching notes’. These were the key attributes or actions he wanted from his coaches. The list was quite different from what you might think and was part of the revolutionary approach he brought to the AFL when he started coaching. He is adamant that he would never have won the 2005 AFL premiership without the list.  \n\n\n\n\nThe list comes from a simple question that Paul suggests that every leader ask themselves: \n\n\n\n\n“Are you the leader you wish you had?” \n\n\n\n\nIt is a question worth asking.  \n\n\n\n\nPaul Roos Coaching Notes (1998): \n\nAlways remember to enjoy what you’re doing. \n\nCoach’s attitude will rub off on the players. \n\nIf coach doesn’t appear happy/relaxed, players will adopt same mentality. \n\nNever lose sight of the fact it is a game of football. \n\nCoach’s job is to set strategies: team plans, team rules, team disciplines, specific instructions to players. \n\nGood communication skills. \n\nTreat people as you want to be treated yourself. \n\nPositive reinforcement to players. \n\nPlayers don’t mean to make mistakes – don’t go out to lose. \n\n42 senior players – all different personalities, deal with each one individually to get the best out of him. \n\nNever drag a player for making a mistake. \n\nDon’t overuse interchange. \n\nPlayers go into a game with different mental approach. \n\nEnjoy training. \n\nMake players accountable for training, discipline, team plans – it is their team too. \n\nWeekly meetings with team leaders. \n\nBe specific at quarter, half, three-quarter time by re-addressing strategies – don’t just verbally abuse. \n\nMotivate players by being positive. \n\nAfter game don’t fly off the handle. If too emotional say nothing, wait until Monday. \n\nSurround yourself with coaches and personnel you know and respect. \n\nBe prepared to listen to advice from advisers. \n\nKeep training interesting and vary when necessary. \n\nTeam bonding and camaraderie is important for a winning team. \n\nMake injured players feel as much a part of the team as possible (players don’t usually make up injuries). \n\nTraining should be game-related. \n\n\n\nRegards\n\nDion Guagliardo | Partner\nFortress Family Office\nAuthorised Representatives\n100 Doors Pty Ltd\nAFSL No. 447657\nwww.fortressfamilyoffice.com")
    page.frame_locator("iframe[title=\"Preview\"]").locator("p").first.click()
    page.frame_locator("iframe[title=\"Preview\"]").locator("div").filter(has_text="One of my favourite parts of").nth(2).press("ControlOrMeta+z")
    page.frame_locator("iframe[title=\"Preview\"]").locator("div").filter(has_text="One of my favourite parts of").nth(2).press("ControlOrMeta+Shift+V")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("One of my favourite parts of").click()
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("One of my favourite parts of").click()
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Debts and Deficits One of my").press("ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Debts and Deficits One of my").press("ArrowUp")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Debts and Deficits One of my").press("ArrowLeft")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Debts and Deficits One of my").press("Home")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Debts and Deficits One of my").press("ArrowUp")
    page.frame_locator("iframe[title=\"Preview\"]").get_by_text("Training should be game-").click(modifiers=["Shift"])
    page.get_by_role("button", name="Save and exit").click()
    page.get_by_role("button", name="Send a Test Email").click()
    page.get_by_role("button", name="Send test").click()
    page.get_by_role("button", name="Ok", exact=True).click()


        # Save storage state for future use
        context.storage_state(path=auth_state_path)
        print("Saved storage state to linkedinAuthState.json")


    postArticle(page)

    page.pause()





with sync_playwright() as playwright:
    run(playwright)
