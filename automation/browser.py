from playwright_stealth.stealth import stealth_async

from playwright.async_api import async_playwright

async def open_google_form(url):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)  # Run in visible mode for debugging
    context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

    page = await context.new_page()
    
    await stealth_async(page)

    
    await page.goto(url)
    return browser, context, page, playwright
