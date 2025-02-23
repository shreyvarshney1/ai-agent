import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://forms.gle/euGW8A8MwAjrfUE39")
        await asyncio.sleep(5)  # Ensure content loads properly
        print(await page.content())  # Print page content

# Ensure proper event loop handling
if __name__ == "__main__":
    asyncio.run(main())
