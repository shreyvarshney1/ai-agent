import json
import os
import re
import time
from openai import OpenAI
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()


def get_mapping(form_fields, user_data):
    prompt = "Here are the form fields:\n"
    for field in form_fields:
        prompt += f"- Label: '{field['label']}', type: {field['type']}"
        if field['type'] in ['select', 'radio', 'checkbox']:
            if field['type'] == 'select':
                options = [text for text in field['options']]
            prompt += f", options: {options}"
        prompt += "\n"
    prompt += f"And here is the user's data: {user_data}\n"
    prompt += (
        "Please provide a mapping where each form field label is a key"
        "For select, radio, and checkbox fields, the value should be value will be used "
        "to select the appropriate option(s).\n"
        "The mapping should be in JSON format."
    )
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("API_KEY")
        )
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers form fields in context to user data. Give answer as a json taking key as 'Label' and value as answer to the question. IF USER CONTEXT IS NOT ENOUGH THAN TRY ANSWERING YOURSELF. YOU CAN ANSWER ACCORDING TO YOUR KNOWLEDGE USING USER DATA AS YOUR CONTEXT."},
                {"role": "user", "content": prompt}
            ]
        )
        mapping_str = response.choices[0].message.content.strip()
        # print(f"Raw response from OpenAI: {mapping_str}")  # Debug response
        pattern = r'(\{([\s\S]+?)\})'
        match = re.search(pattern, mapping_str, re.DOTALL)
        if match:
            json_str = match.group(1)
            print(json_str)
            data = json.loads(json_str)
            return data
        else:
            print("No JSON block found.")
            return {}
    except Exception as e:
        print(f"Error getting mapping from OpenAI: {e}")
        return {}


def evaluate_expression(expr, user_data):
    """
    Evaluate an expression that combines user data keys (e.g., 'first_name + " " + last_name').

    Args:
        expr: String expression to evaluate.
        user_data: Dictionary of user data.

    Returns:
        Evaluated string value.
    """
    try:
        parts = expr.split('+')
        value = ''
        for part in parts:
            part = part.strip()
            if part.startswith("'") and part.endswith("'"):
                value += part[1:-1]
            elif part in user_data:
                value += str(user_data[part])
            else:
                raise ValueError(f"Unknown part in expression: {part}")
        return value
    except Exception as e:
        print(f"Error evaluating expression '{expr}': {e}")
        return ""


def fill_form(url, mapping):
    with sync_playwright() as p:
        # Change to False to see the browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        field_elements = page.query_selector_all("div[role='listitem']")

        for field in field_elements:
            try:
                title = field.query_selector(
                    "div[role='heading']").inner_text().split("\n")[0].strip()
            except Exception:
                title = "Unknown"
            if not mapping[title]:
                print(f"No mapping found for field '{title}', skipping.")
                continue

            map_value = mapping[title]
            try:
                if field.query_selector("input[type='text'], textarea"):
                    field.query_selector(
                        "input[type='text'], textarea").fill(map_value)
                elif field.query_selector("div[role='radiogroup']"):
                    option_elements = field.query_selector("div[role='radio']")
                    for option in option_elements:
                        opt_text = option.inner_text().strip()
                        if opt_text == map_value:
                            option.check()
                elif field.query_selector("div[role='listbox']"):
                    dropdown = field.query_selector("div[role='listbox']")
                    dropdown.click()
                    time.sleep(1)
                    option_elements = page.query_selector_all(
                        "div[role='option']")
                    for option in option_elements:
                        opt_text = option.inner_text().strip()
                        if opt_text == map_value:
                            option.click()
                            time.sleep(2)
                elif field.query_selector("div[role='checkbox']"):
                    option_elements = field.query_selector(
                        "div[role='checkbox']")
                    for option in option_elements:
                        opt_text = option.inner_text().strip()
                        if opt_text == map_value:
                            option.check()
            except Exception as e:
                print(f"Error filling field '{title}': {e}")
        try:
            page.query_selector("div[aria-label='Submit']").click()
            print("Form submitted successfully.")
        except Exception as e:
            print(f"Error clicking submit button: {e}")
        time.sleep(2)
        browser.close()
