from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8501")

    # Take a screenshot of the initial page
    page.screenshot(path="jules-scratch/verification/streamlit_upload_page.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
