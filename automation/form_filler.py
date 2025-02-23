def fill_form(page, form_data):
    """
    Fills and submits the form using provided form_data.
    Skips any element that is not visible.
    """
    for field, value in form_data.items():
        input_element = page.locator(f'[name="{field}"], [id="{field}"]')
        
        # Skip if element is hidden
        if not input_element.is_visible():
            print(f"⚠️ Skipping field '{field}' because it's not visible.")
            continue
        
        input_element.fill(value)
    
    # Click the submit button (adjust selector as needed)
    page.locator('button[type="submit"]').click()
