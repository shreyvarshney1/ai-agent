from browser import open_browser
from form_parser import get_form_fields
from form_filler import fill_form
from llm_helper import predict_field_value

def main():
    url = "https://docs.google.com/forms/d/e/1FAIpQLSen6AIaYLHM-u4PFhK7xy8SP7KRtyJVPPeqTb0Uz52ph0uY7A/viewform?usp=sharing"
    browser, context, page = open_browser(url)  # Keeping context

    try:
        # Extract form fields
        fields = get_form_fields(page)
        
        # Predict field values using Gemini API
        form_data = {key: predict_field_value(key, "Provide appropriate data") for key in fields.keys()}
        
        # Fill and submit the form
        fill_form(page, form_data)
    
    finally:
        # Ensure context and browser are closed properly
        context.close()
        browser.close()

if __name__ == "__main__":
    main()
