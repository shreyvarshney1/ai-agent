import google.generativeai as genai
import os

# Set the Gemini API key (replace with your actual key)
API_KEY = "AIzaSyAGfIb2eay3NSlnoA-sRR_mpQKxkF2a8Bg"  # 🔹 Replace this with a valid key
genai.configure(api_key=API_KEY)
if not API_KEY:
    raise ValueError("❌ ERROR: No API key found. Set GEMINI_API_KEY environment variable.")

genai.configure(api_key=API_KEY)
if not API_KEY:
    raise ValueError("❌ ERROR: No API key found. Set GEMINI_API_KEY environment variable.")

genai.configure(api_key=API_KEY)

def predict_field_value(field_name, prompt):
    """
    Uses Gemini API to predict a field value.
    If blocked, returns a default value.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Field Name: {field_name}\nPrompt: {prompt}\nProvide only a single, clear response.")

        # Check if response is valid
        if not response.candidates or response.candidates[0].finish_reason != "STOP":
            print(f"⚠️ Warning: Gemini API blocked the request for '{field_name}'. Using default value.")
            return "N/A"

        return response.text.strip()

    except Exception as e:
        print(f"❌ Error in predicting field '{field_name}': {e}")
        return "N/A"