from playwright.sync_api import sync_playwright
import time

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
            options = []
            # Debugging: Print detected field name
            # print(f"[DEBUG] Found Field: {title}")

            try:
                if field.query_selector("input[type='text'], textarea"):
                    field_type = "text"
                elif field.query_selector("div[role='radiogroup']"):
                    field_type = "radio"
                    option_elements = field.query_selector("div[role='radio']")
                    for option in option_elements:
                        opt_text = option.inner_text().strip()
                        if opt_text:
                            options.append(opt_text)
                elif field.query_selector("div[role='checkbox']"):
                    field_type = "checkbox"
                    option_elements = field.query_selector("div[role='checkbox']")
                    for option in option_elements:
                        opt_text = option.inner_text().strip()
                        if opt_text:
                            options.append(opt_text)
                elif field.query_selector("div[role='listbox']"):
                    field_type = "select"
                    dropdown = field.query_selector("div[role='listbox']")
                    dropdown.click()  # Open the dropdown
                    time.sleep(1)  # Allow the dropdown to open
                    
                    try:
                        # First, try locating the popup container with the typical Google Forms class
                        popup_container = page.query_selector("div.exportSelectPopup")
                        option_elements = popup_container.query_selector_all("div.exportSelectPopupOption")
                    except Exception as e:
                        print("[DEBUG] Could not locate 'exportSelectPopup' container, trying fallback for dropdown options.")
                        # Fallback: look for any elements with role='option'
                        time.sleep(1)
                        option_elements = page.query_selector_all("div[role='option']")
                    
                    for option in option_elements:
                        opt_text = option.inner_text().strip()
                        # Filter out the default placeholder (e.g., "Choose")
                        if opt_text and opt_text.lower() != "choose":
                            options.append(opt_text)
                            
                    # Close the dropdown by clicking outside (e.g., the body)
                    page.click("body")
            except Exception as e:
                print(
                    f"[ERROR] Failed to determine input type for {title}: {e}")

            form_fields.append({"label": title, "type": field_type, "options": options})

        browser.close()
        return form_fields
