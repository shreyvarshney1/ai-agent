import cv2
import pytesseract
import numpy as np
from playwright.sync_api import sync_playwright

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """Enhance image for better OCR accuracy"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return gray

def extract_text_from_image(image_path):
    """Extract text using Tesseract with better OCR settings"""
    processed_image = preprocess_image(image_path)
    extracted_text = pytesseract.image_to_string(processed_image, lang="eng", config="--psm 6 --oem 3")
    return extracted_text.strip()

def extract_google_form_fields(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        form_fields = []
        field_elements = page.query_selector_all("div[role='listitem']")

        for index, field in enumerate(field_elements):
            label_text = field.inner_text().strip()

            # OCR fallback if label extraction fails
            if not label_text or len(label_text) < 3:
                filename = f"field_{index}.png"
                field.screenshot(path=filename)
                label_text = extract_text_from_image(filename)

            # Detect input types correctly
            input_element = field.query_selector("input")
            textarea_element = field.query_selector("textarea")
            radio_element = field.query_selector("div[role='radiogroup']")
            dropdown_element = field.query_selector("div[role='combobox']")  # Google Forms uses combobox for dropdowns

            if input_element or textarea_element:
                input_type = "text"
            elif radio_element:
                input_type = "radio"
            elif dropdown_element:
                input_type = "dropdown"
            else:
                input_type = "unknown"  # Should be rare now

            form_fields.append({"label": label_text, "input_type": input_type})

        browser.close()
        return form_fields

if __name__ == "__main__":
    google_form_url = "https://forms.gle/euGW8A8MwAjrfUE39"  # Replace with actual form link
    fields = extract_google_form_fields(google_form_url)

    print("\nExtracted Google Form Fields:\n")
    for field in fields:
        print(f"Field Name: {field['label']} | Input Type: {field['input_type']}")
