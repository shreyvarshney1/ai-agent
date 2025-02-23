from playwright.sync_api import sync_playwright
from llm_helper import predict_field_value
from form_filler import fill_form
from form_parser import get_form_fields
from playwright.sync_api import sync_playwright

_playwright = sync_playwright().start()  # Keep Playwright active globally

def open_browser(url):
    """Opens a browser context and navigates to the given URL."""
    browser = _playwright.chromium.launch(headless=False)
    context = browser.new_context()  # Create a new context
    page = context.new_page()
    page.goto(url)
    return browser, context, page  # Return all objects properly

def handle_multiple_tabs(urls):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        pages = [context.new_page() for _ in urls]
        
        for page, url in zip(pages, urls):
            page.goto(url)
            fields = get_form_fields(page)
            form_data = {key: predict_field_value(key, "Provide appropriate data") for key in fields.keys()}
            fill_form(page, form_data)

        browser.close()
