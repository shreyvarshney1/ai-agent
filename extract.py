from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from playwright.sync_api import sync_playwright

def open_google_form_selenium(url):
    """
    Extract form fields from a Google Form using Selenium and Playwright.
    
    Args:
        driver: Selenium WebDriver instance
        url: URL of the Google Form
        
    Returns:
        List of dictionaries containing field details
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to False to see the browser
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        form_fields = []

        # Select all form fields
        field_elements = page.query_selector_all("div[role='listitem']")

        for index, field in enumerate(field_elements):
            # Extract field label (try multiple selectors)
            label_element = field.query_selector("div.M7eMe, div[role='heading']")
            label = label_element.inner_text() if label_element else "Unknown Field"

            # Extract input type
            input_element = field.query_selector("input, textarea, select")
            if input_element:
                input_type = input_element.get_attribute("type") or "text"
            else:
                input_type = "unknown"

            form_fields.append({
                "label": label,
                "type": input_type
            })

        browser.close()
        return form_fields
