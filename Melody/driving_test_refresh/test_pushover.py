import asyncio
import os
import sys
from pathlib import Path
import httpx
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")


async def test_pushover():
    """Test Pushover notification."""
    print(f"PUSHOVER_USER: {'✓ Set' if PUSHOVER_USER else '✗ Not set'}")
    print(f"PUSHOVER_TOKEN: {'✓ Set' if PUSHOVER_TOKEN else '✗ Not set'}")

    if not PUSHOVER_USER or not PUSHOVER_TOKEN:
        print("\n❌ Error: PUSHOVER_USER and PUSHOVER_TOKEN must be set in .env file")
        return False

    async with httpx.AsyncClient() as client:
        try:
            print("\nSending test notification...")
            response = await client.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": PUSHOVER_TOKEN,
                    "user": PUSHOVER_USER,
                    "message": "This is a test notification from your driving test monitor script!",
                    "title": "🧪 Test Notification",
                },
            )
            response.raise_for_status()
            print("✓ Notification sent successfully!")
            print(f"Response: {response.json()}")
            return True
        except Exception as e:
            print(f"✗ Failed to send notification: {e}")
            return False


if __name__ == "__main__":
    asyncio.run(test_pushover())
