from playwright.sync_api import sync_playwright

def test_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://localhost:8000/index.html")  # Change if needed
        
        # Fill the form
        page.fill("input[name='name']", "John Doe")
        page.fill("input[name='email']", "john@example.com")
        page.fill("input[name='age']", "25")
        page.click("button[type='submit']")
        
        print("Form submitted successfully!")
        browser.close()

test_form()
