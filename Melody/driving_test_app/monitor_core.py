"""
Core monitoring logic for driving test slot availability.
Refactored to be used with Gradio UI.
"""
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
import httpx
from typing import Callable, Optional


class DrivingTestMonitor:
    """Monitor driving test booking page for available slots."""

    TARGET_URL = "https://www.myrta.com/wps/portal/extvp/myrta/licence/tbs/tbs-change/!ut/p/z1/hZBfT4MwFMU_kbsFHOAjf7bBHIOw0dm-LFXrrIOWQAX008s08cFkeN_Oye_cnByg8ABUsk6cmBZKsnLUhNpHFC0yXJiO4VrzEMXLwPGNNDOQZwGGww9y5TwEdPoDGfPOcZ0tsmQTuUYa342p202Qx2FirnILCqmaauyyAwr0jXVsmNWq0SXXM9YCMS-2qOpSPAmdqGdeAtHNO7_Ykg8aC94D4VLzJuSaibIdK9PJVvfWXwDtYhvFfoFT7FmGu_8HWNm_wPVd1kAflTp7e97q4JXJE4eDD6QPkHjpv2ednKWulu6wnXfbm3MefWYfXzzIDeE!/"
    NO_SLOTS_TEXT = "There are no timeslots available for this week."

    def __init__(
        self,
        booking_id: str,
        family_name: str,
        preferred_date: str,
        suburb: str,
        suburb_dropdown_option: str,
        check_interval: int = 5,
        pushover_user: Optional[str] = None,
        pushover_token: Optional[str] = None,
        log_callback: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialize the monitor.

        Args:
            booking_id: Booking ID number
            family_name: Family name for login
            preferred_date: Preferred date in DD/MM/YYYY format
            suburb: Suburb name to search
            suburb_dropdown_option: Suburb option text to select from dropdown
            check_interval: Seconds between checks (default: 5)
            pushover_user: Pushover user key (optional)
            pushover_token: Pushover API token (optional)
            log_callback: Callback function for log messages
        """
        self.booking_id = booking_id
        self.family_name = family_name
        self.preferred_date = preferred_date
        self.suburb = suburb
        self.suburb_dropdown_option = suburb_dropdown_option
        self.check_interval = check_interval
        self.pushover_user = pushover_user
        self.pushover_token = pushover_token
        self.log_callback = log_callback

        self._stop_flag = False
        self._running = False

    def log(self, message: str):
        """Log a message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        print(full_message)
        if self.log_callback:
            self.log_callback(full_message)

    async def send_pushover_notification(self, message: str, title: str = "Driving Test Alert"):
        """Send a Pushover notification."""
        if not self.pushover_user or not self.pushover_token:
            self.log("⚠ Pushover credentials not provided - skipping notification")
            return False

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.pushover.net/1/messages.json",
                    data={
                        "token": self.pushover_token,
                        "user": self.pushover_user,
                        "message": message,
                        "title": title,
                    },
                )
                response.raise_for_status()
                self.log(f"✓ Notification sent: {message}")
                return True
            except Exception as e:
                self.log(f"✗ Failed to send notification: {e}")
                return False

    async def initial_login(self, page):
        """Perform initial login and navigation to the booking page."""
        try:
            self.log("Loading page...")
            await page.goto(self.TARGET_URL, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(2)

            # Fill in booking number
            self.log("  → Filling booking number...")
            booking_input = await page.wait_for_selector('input[name="bookingId"]', timeout=10000)
            await booking_input.fill(self.booking_id)
            await asyncio.sleep(0.5)

            # Fill in family name
            self.log("  → Filling family name...")
            surname_input = await page.wait_for_selector('input[name="surname"]', timeout=10000)
            await surname_input.fill(self.family_name)
            await asyncio.sleep(0.5)

            # Wait 3 seconds after entering login details
            self.log("  → Waiting 3 seconds...")
            await asyncio.sleep(3)

            # Click continue button
            self.log("  → Clicking continue button...")
            continue_button = await page.wait_for_selector('span#submitNoLogin_label', timeout=10000)
            await continue_button.click()
            await asyncio.sleep(2)

            # Click change location button
            self.log("  → Clicking change location button...")
            change_location_button = await page.wait_for_selector('span#changeLocationButton_label', timeout=10000)
            await change_location_button.click()
            await asyncio.sleep(2)

            # Enter preferred date
            self.log(f"  → Entering preferred date: {self.preferred_date}...")
            date_input = await page.wait_for_selector('input[name="preferredDateStr"]', timeout=10000)
            await date_input.fill(self.preferred_date)
            await asyncio.sleep(0.5)

            # Click suburb radio button
            self.log("  → Selecting suburb search option...")
            suburb_radio = await page.wait_for_selector('input#rms_batLocPostSel[name="testHGroup"]', timeout=10000)
            await suburb_radio.click()
            await asyncio.sleep(1)

            # Enter suburb name letter by letter
            self.log(f"  → Typing suburb '{self.suburb}' letter by letter...")
            suburb_input = await page.wait_for_selector('input#inputSuburbName', timeout=10000)
            await suburb_input.click()
            await suburb_input.type(self.suburb, delay=100)
            await asyncio.sleep(1)

            # Wait for and click the dropdown option
            self.log(f"  → Selecting {self.suburb_dropdown_option} from dropdown...")
            suburb_option = await page.wait_for_selector(
                f'li[id^="inputSuburbName_popup"]:has-text("{self.suburb_dropdown_option}")',
                timeout=10000
            )
            await suburb_option.click()
            await asyncio.sleep(1)

            # Click "Find a location" button
            self.log("  → Clicking 'Find a location'...")
            find_location_button = await page.wait_for_selector('span#verifyTestLoc_label', timeout=10000)
            await find_location_button.click()
            await asyncio.sleep(2)

            # Select location radio button by suburb name
            self.log(f"  → Selecting {self.suburb_dropdown_option} location...")
            location_label = await page.wait_for_selector(
                f'label:has-text("{self.suburb_dropdown_option}")',
                timeout=10000
            )
            await location_label.click()
            await asyncio.sleep(1)

            # Click Next button
            self.log("  → Clicking 'Next'...")
            next_button = await page.wait_for_selector('span#nextButton_label', timeout=10000)
            await next_button.click()
            await asyncio.sleep(3)

            self.log("✓ Initial setup complete - now on booking page")
            return True

        except Exception as e:
            self.log(f"⚠ Error during initial login: {e}")
            return False

    async def check_for_slots(self, page, check_count):
        """Check the current page for available timeslots."""
        try:
            self.log(f"Check #{check_count}: Refreshing page...")
            await page.reload(wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(2)

            # Get the page content
            content = await page.content()

            # Check if the "no timeslots" message is present
            if self.NO_SLOTS_TEXT not in content:
                self.log("🎉 TIMESLOTS AVAILABLE!")
                message = f"Timeslots are now available for booking!\n\nURL: {self.TARGET_URL}"
                await self.send_pushover_notification(message, "🎉 Driving Test Slots Available!")
                self.log("✓ Slots found! Browser will remain open for booking.")
                return True
            else:
                self.log("⏳ No timeslots available yet...")
                return False

        except Exception as e:
            self.log(f"⚠ Error during check: {e}")
            return False

    def stop(self):
        """Stop the monitoring."""
        self._stop_flag = True
        self.log("Stop signal received...")

    def is_running(self):
        """Check if monitor is running."""
        return self._running

    async def start(self):
        """Start monitoring for available slots."""
        if self._running:
            self.log("Monitor is already running!")
            return

        self._running = True
        self._stop_flag = False

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            self.log(f"Starting monitoring at {self.TARGET_URL}")
            self.log(f"Checking every {self.check_interval} seconds...")
            self.log(f"Looking for absence of: '{self.NO_SLOTS_TEXT}'")
            self.log("-" * 60)

            try:
                # Perform initial login and navigation
                login_success = await self.initial_login(page)

                if not login_success:
                    self.log("❌ Initial login failed")
                    self._running = False
                    await browser.close()
                    return

                # Now continuously check for slots by refreshing
                check_count = 0
                slots_found = False

                while not self._stop_flag:
                    check_count += 1

                    # Check for available slots
                    found_slots = await self.check_for_slots(page, check_count)

                    if found_slots and not slots_found:
                        slots_found = True
                        self.log("🎯 Browser will remain open for booking.")
                        self.log("Click 'Stop Monitoring' when you're done.")
                        # Keep browser open but stop refreshing
                        break

                    # Wait before next check
                    self.log(f"  → Waiting {self.check_interval} seconds before next check...")

                    # Check stop flag every second during wait
                    for _ in range(self.check_interval):
                        if self._stop_flag:
                            break
                        await asyncio.sleep(1)

                # If slots found, wait for user to manually stop
                if slots_found:
                    while not self._stop_flag:
                        await asyncio.sleep(1)

                self.log("⏹ Monitoring stopped")

            except Exception as e:
                self.log(f"❌ Error: {e}")
            finally:
                self._running = False
                await browser.close()
                self.log("Browser closed")
