import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.linkedin.com/login")
    page.get_by_label("Email or phone").fill("dion@100doors.co")
    page.get_by_label("Password", exact=True).fill("Paula$1977")
    page.get_by_label("Sign in", exact=True).click()
    page.get_by_label("Write an article on LinkedIn").click()
    page.get_by_role("radio", name="Dion Guagliardo").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_placeholder("Title").fill("Test Title")
    page.get_by_label("Write here. You can also").click()
    page.get_by_label("Article editor content").fill("test content")
    # page.get_by_role("group", name="We recommend uploading or").locator("label").click()
    # page.get_by_label("Upload from computer").set_input_files("COOKING APP (1).png")
    page.get_by_label("Article editor content").press("Tab")    
    page.get_by_role("button", name="Next").click()
    page.get_by_role("paragraph").click()
    page.get_by_label("Text editor for creating").fill("Test intro para")


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
