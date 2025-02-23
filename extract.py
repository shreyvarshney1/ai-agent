from playwright.sync_api import sync_playwright
from selenium.webdriver.common.by import By


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
        # Change to False to see the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        form_fields = []

        # Select all form fields
        field_elements = page.query_selector_all("div[role='listitem']")

        for field in field_elements:
            try:
                title = field.query_selector("div[role='heading']").inner_text().split("\n")[0].strip()
            except Exception:
                title = "Unknown"

            field_type = "unknown"

            # Debugging: Print detected field name
            # print(f"[DEBUG] Found Field: {title}")

            try:
                if field.query_selector("input[type='text'], textarea"):
                    field_type = "text"
                elif field.query_selector("div[role='radiogroup']"):
                    field_type = "radio"
                elif field.query_selector("div[role='checkbox']"):
                    field_type = "checkbox"
                elif field.query_selector("div[role='listbox']"):
                    field_type = "select"
            except Exception as e:
                print(
                    f"[ERROR] Failed to determine input type for {title}: {e}")

            form_fields.append({"label": title, "type": field_type})

        browser.close()
        return form_fields
