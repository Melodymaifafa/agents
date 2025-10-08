import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright
import httpx
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
TARGET_URL = "https://www.myrta.com/wps/portal/extvp/myrta/licence/tbs/tbs-change/!ut/p/z1/hZBfT4MwFMU_kbsFHOAjf7bBHIOw0dm-LFXrrIOWQAX008s08cFkeN_Oye_cnByg8ABUsk6cmBZKsnLUhNpHFC0yXJiO4VrzEMXLwPGNNDOQZwGGww9y5TwEdPoDGfPOcZ0tsmQTuUYa342p202Qx2FirnILCqmaauyyAwr0jXVsmNWq0SXXM9YCMS-2qOpSPAmdqGdeAtHNO7_Ykg8aC94D4VLzJuSaibIdK9PJVvfWXwDtYhvFfoFT7FmGu_8HWNm_wPVd1kAflTp7e97q4JXJE4eDD6QPkHjpv2ednKWulu6wnXfbm3MefWYfXzzIDeE!/"
CHECK_INTERVAL = 5  # seconds
NO_SLOTS_TEXT = "There are no timeslots available for this week."


async def send_pushover_notification(message: str, title: str = "Driving Test Alert"):
    """Send a Pushover notification."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": PUSHOVER_TOKEN,
                    "user": PUSHOVER_USER,
                    "message": message,
                    "title": title,
                },
            )
            response.raise_for_status()
            print(f"✓ Notification sent: {message}")
            return True
        except Exception as e:
            print(f"✗ Failed to send notification: {e}")
            return False


async def initial_login(page):
    """Perform initial login and navigation to the booking page."""
    try:
        print("\n[Initial Setup] Loading page...")
        await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)

        # Wait a bit for page to settle
        await asyncio.sleep(2)

        # Fill in booking number
        print("  → Filling booking number...")
        booking_input = await page.wait_for_selector('input[name="bookingId"]', timeout=10000)
        await booking_input.fill("2931865745")
        await asyncio.sleep(0.5)

        # Fill in family name
        print("  → Filling family name...")
        surname_input = await page.wait_for_selector('input[name="surname"]', timeout=10000)
        await surname_input.fill("Qi")
        await asyncio.sleep(0.5)

        # Wait 3 seconds after entering login details
        print("  → Waiting 3 seconds...")
        await asyncio.sleep(3)

        # Click continue button
        print("  → Clicking continue button...")
        continue_button = await page.wait_for_selector('span#submitNoLogin_label', timeout=10000)
        await continue_button.click()
        await asyncio.sleep(2)

        # Click change location button
        print("  → Clicking change location button...")
        change_location_button = await page.wait_for_selector('span#changeLocationButton_label', timeout=10000)
        await change_location_button.click()
        await asyncio.sleep(2)

        # Click suburb radio button
        print("  → Selecting suburb search option...")
        suburb_radio = await page.wait_for_selector('input#rms_batLocPostSel[name="testHGroup"]', timeout=10000)
        await suburb_radio.click()
        await asyncio.sleep(1)

        # Enter suburb name letter by letter
        print("  → Typing suburb 'lidcombe' letter by letter...")
        suburb_input = await page.wait_for_selector('input#inputSuburbName', timeout=10000)
        await suburb_input.click()
        await suburb_input.type("lidcombe", delay=100)  # 100ms delay between each keystroke
        await asyncio.sleep(1)

        # Wait for and click the dropdown option LIDCOMBE, 2141
        print("  → Selecting LIDCOMBE, 2141 from dropdown...")
        lidcombe_option = await page.wait_for_selector('li[id^="inputSuburbName_popup"]:has-text("LIDCOMBE, 2141")', timeout=10000)
        await lidcombe_option.click()
        await asyncio.sleep(1)

        # Click "Find a location" button
        print("  → Clicking 'Find a location'...")
        find_location_button = await page.wait_for_selector('span#verifyTestLoc_label', timeout=10000)
        await find_location_button.click()
        await asyncio.sleep(2)

        # Select LIDCOMBE 2141 location radio button
        print("  → Selecting LIDCOMBE 2141 location...")
        lidcombe_location_radio = await page.wait_for_selector('input#rms_batLocLoc_601', timeout=10000)
        await lidcombe_location_radio.click()
        await asyncio.sleep(1)

        # Click Next button
        print("  → Clicking 'Next'...")
        next_button = await page.wait_for_selector('span#nextButton_label', timeout=10000)
        await next_button.click()

        # Wait for page to load
        await asyncio.sleep(3)

        print("✓ Initial setup complete - now on booking page")
        return True

    except Exception as e:
        print(f"⚠ Error during initial login: {e}")
        return False


async def check_for_slots(page, check_count):
    """Check the current page for available timeslots."""
    try:
        print(f"\n[Check #{check_count}] Refreshing page...")
        await page.reload(wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)

        # Get the page content
        content = await page.content()

        # Check if the "no timeslots" message is present
        if NO_SLOTS_TEXT not in content:
            print("🎉 TIMESLOTS AVAILABLE!")
            message = f"Timeslots are now available for booking!\n\nURL: {TARGET_URL}"
            await send_pushover_notification(message, "🎉 Driving Test Slots Available!")
            print("\n✓ Slots found! Browser will remain open for booking.")
            print("Press Ctrl+C to stop monitoring...")
            return True
        else:
            print("⏳ No timeslots available yet...")
            return False

    except Exception as e:
        print(f"⚠ Error during check: {e}")
        return False


async def check_page():
    """Check the page for timeslot availability."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print(f"Starting monitoring at {TARGET_URL}")
        print(f"Checking every {CHECK_INTERVAL} seconds...")
        print(f"Looking for absence of: '{NO_SLOTS_TEXT}'")
        print("-" * 60)

        try:
            # Perform initial login and navigation
            login_success = await initial_login(page)

            if not login_success:
                print("❌ Initial login failed")
                return

            # Now continuously check for slots by refreshing
            check_count = 0
            while True:
                check_count += 1

                # Check for available slots
                found_slots = await check_for_slots(page, check_count)

                if found_slots:
                    # Slots found - stop refreshing and keep browser open
                    print("\n🎯 Browser will remain open. Press Ctrl+C when done.")
                    # Wait indefinitely until user closes
                    while True:
                        await asyncio.sleep(3600)  # Sleep for 1 hour intervals

                # Wait before next check
                print(f"  → Waiting {CHECK_INTERVAL} seconds before next check...")
                await asyncio.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n⏹ Monitoring stopped by user")
        finally:
            await browser.close()


async def main():
    # Validate environment variables
    if not PUSHOVER_USER or not PUSHOVER_TOKEN:
        print("❌ Error: PUSHOVER_USER and PUSHOVER_TOKEN must be set in .env file")
        sys.exit(1)

    await check_page()


if __name__ == "__main__":
    asyncio.run(main())
