from playwright.sync_api import sync_playwright
import time


def open_google_form(url):
    with sync_playwright() as p:
        # Change to False to see the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        form_fields = []
        field_elements = page.query_selector_all("div[role='listitem']")

        for field in field_elements:
            try:
                title = field.query_selector(
                    "div[role='heading']").inner_text().split("\n")[0].strip()
            except Exception:
                title = "Unknown"

            field_type = "unknown"
            options = []
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
                    option_elements = field.query_selector(
                        "div[role='checkbox']")
                    for option in option_elements:
                        opt_text = option.inner_text().strip()
                        if opt_text:
                            options.append(opt_text)
                elif field.query_selector("div[role='listbox']"):
                    field_type = "select"
                    dropdown = field.query_selector("div[role='listbox']")
                    dropdown.click()
                    time.sleep(1)
                    option_elements = page.query_selector_all(
                        "div[role='option']")

                    for option in option_elements:
                        opt_text = option.inner_text().strip()
                        if opt_text and opt_text.lower() != "choose":
                            options.append(opt_text)

                    page.click("body")
            except Exception as e:
                print(
                    f"[ERROR] Failed to determine input type for {title}: {e}")

            form_fields.append(
                {"label": title, "type": field_type, "options": options})

        browser.close()
        return form_fields
