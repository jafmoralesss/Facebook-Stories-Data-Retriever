import asyncio
from playwright.async_api import async_playwright
async def capture_session():
    print("Capturando sesión...")

    async with async_playwright() as p:

        #Navigator launch
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        #Getting to Facebook
        print("Entering Facebook account...")
        await page.goto("https://www.facebook.com/")

        print("\n" +"="*50)
        print("MANUAL INTERACTION REQUIRED")
        print("1. Check the new window")
        print("2. Log in with your user and password")
        print("3. Approbe two steps verification if needed")
        print("4. Navigate to the Feed")
        print("5. Go to the terminal and press ENTER")
        print("="*50+"\n")

        await asyncio.to_thread(input, "Press ENTER when log in has been completed")

        await context.storage_state(path="facebook_auth.json")
        print("SUCCESS. Session saved in 'facebook_auth.json'.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_session())