import os
import openai
from dotenv import load_dotenv

from extract import open_google_form
from form_filler import get_mapping, fill_form

load_dotenv()
openai.api_key = os.getenv("API_KEY")


def main(form_url, user_data):
    try:
        form_fields = open_google_form(form_url)

        if not form_fields:
            print("No form fields found.")
            return
        mapping = get_mapping(form_fields, user_data)

        if not mapping:
            print("Failed to get field mapping.")
            return
        fill_form(form_url, mapping)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    form_url = "https://forms.gle/NryNa3ZWmM8WfiwPA"

    try:
        user_data = open("user_data.txt", "r").read()
    except:
        user_data = {}

    if not openai.api_key:
        print("Please set the API_KEY environment variable.")
    else:
        main(form_url, user_data)
