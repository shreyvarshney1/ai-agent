import json
import os
import openai
from selenium.webdriver.support.ui import Select
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_mapping(form_fields, user_data):
    """
    Use OpenAI API to map form fields to user data.
    
    Args:
        form_fields: List of dictionaries containing field details.
        user_data: Dictionary of user data to map to form fields

    Returns:
        Dictionary mapping field labels to user data keys or expressions.
    """
    # Construct the prompt for OpenAI
    prompt = "Here are the form fields:\n"
    for field in form_fields:
        prompt += f"- Label: '{field['label']}', type: {field['type']}"
        if field['type'] in ['select', 'radio', 'checkbox']:
            if field['type'] == 'select':
                options = [opt.text for opt in Select(field['element']).options if opt.text]
            else:
                options = [text for text, _ in field['options']]
            prompt += f", options: {options}"
        prompt += "\n"
    prompt += f"And here is the user's data: {user_data}\n"
    prompt += (
        "Please provide a mapping where each form field label is a key, and its value is the "
        "corresponding user data key or an expression that combines user data keys to get the value for that field.\n"
        "For select, radio, and checkbox fields, the value should be the user data key whose value will be used "
        "to select the appropriate option(s).\n"
        "The mapping should be in JSON format."
    )
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key= os.getenv("API_KEY")
        )
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that maps form fields to user data."},
                {"role": "user", "content": prompt}
            ]
        )
        mapping_str = response.choices[0].message.content.strip()
        mapping = json.loads(mapping_str)
        return mapping
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

def fill_form(form_fields, mapping, user_data):
    """
    Fill the form fields based on the AI-generated mapping.
    
    Args:
        driver: Selenium WebDriver instance.
        form_fields: List of dictionaries containing field details.
        mapping: Dictionary mapping labels to user data keys or expressions.
        user_data: Dictionary of user data.
    """
    for field in form_fields:
        label = field['label']
        if label not in mapping or not mapping[label]:
            print(f"No mapping found for field '{label}', skipping.")
            continue
        
        map_value = mapping[label]
        try:
            if field['type'] == 'text':
                if '+' in map_value:
                    value = evaluate_expression(map_value, user_data)
                else:
                    value = user_data[map_value]
                field['element'].send_keys(value)
            elif field['type'] == 'select':
                value = user_data[map_value]
                Select(field['element']).select_by_visible_text(value)
            elif field['type'] == 'radio':
                value = user_data[map_value]
                for option_text, input_element in field['options']:
                    if option_text == value:
                        input_element.click()
                        break
                else:
                    print(f"Option '{value}' not found for radio field '{label}'.")
            elif field['type'] == 'checkbox':
                values = user_data[map_value]
                if not isinstance(values, list):
                    values = [values]
                for option_text, input_element in field['options']:
                    if option_text in values:
                        input_element.click()
        except Exception as e:
            print(f"Error filling field '{label}': {e}")