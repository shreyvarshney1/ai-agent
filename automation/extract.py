import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from playwright.sync_api import sync_playwright

def extract_form_fields(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to False to see the browser
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        form_fields = []

        # Select all form fields
        field_elements = page.query_selector_all("div[role='listitem']")

        for index, field in enumerate(field_elements):
            print(f"\nDEBUG: Field {index + 1}: {field.inner_text()}")  # Debugging

            # Extract field label (try multiple selectors)
            label_element = field.query_selector("div.M7eMe, div[role='heading']")
            label = label_element.inner_text() if label_element else "Unknown Field"

            # Extract input type
            input_element = field.query_selector("input, textarea, select")
            if input_element:
                input_type = input_element.get_attribute("type") or "text"
            else:
                input_type = "unknown"

            form_fields.append({"label": label, "input_type": input_type})

        browser.close()
        return form_fields

def open_google_form_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(3)  # Allow the page to load

    # Extract form fields using Playwright
    fields = extract_form_fields(url)

    print("\nExtracted Google Form Fields:\n")
    for field in fields:
        print(f"Field Name: {field['label']} | Input Type: {field['input_type']}")

    driver.quit()

if __name__ == "__main__":
    google_form_url = "https://forms.gle/euGW8A8MwAjrfUE39"  # Replace with actual Google Form link
    open_google_form_selenium(google_form_url)
