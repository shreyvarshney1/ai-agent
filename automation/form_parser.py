from playwright.async_api import Page

async def get_form_elements(page: Page):
    await page.wait_for_selector('form')  # Wait for the form to be visible
    elements = await page.query_selector_all('input, textarea, select, button')
    return [await el.evaluate("el => el.outerHTML") for el in elements]
