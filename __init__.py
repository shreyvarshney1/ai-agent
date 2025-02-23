import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import openai
from dotenv import load_dotenv

# Import modules
from extract import open_google_form_selenium
from form_filler import get_mapping, fill_form, evaluate_expression

load_dotenv()
openai.api_key = os.getenv("API_KEY")

def main(form_url, user_data):
    """
    Main function to orchestrate the form-filling process.

    Args:
        form_url: URL of the Google Form to fill.
        user_data: Dictionary of user data to populate the form.
    """
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no browser UI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return

    try:
        # Open Google Form and extract fields
        form_fields = open_google_form_selenium(driver, form_url)
        
        if not form_fields:
            print("No form fields found.")
            return
            
        # Get AI mapping for form fields
        mapping = get_mapping(form_fields, user_data)
        
        if not mapping:
            print("Failed to get field mapping.")
            return

        # Fill form fields
        fill_form(driver, form_fields, mapping, user_data)
        
        # Submit form
        try:
            submit_button = driver.find_element(
                By.XPATH, "//div[@role='button' and contains(., 'Submit')]")
            submit_button.click()
            print("Form submitted successfully.")
        except Exception as e:
            print(f"Error submitting form: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    # Example usage
    form_url = "https://forms.gle/NryNa3ZWmM8WfiwPA"
    user_data = {
        'first_name': 'Shrey',
        'last_name': 'Varshney',
        'email': 'john@example.com',
        'country': 'USA',
        'gender': 'Male',
        'interests': ['Sports', 'Reading']
    }

    if not openai.api_key:
        print("Please set the API_KEY environment variable.")
    else:
        main(form_url, user_data)
