# Driving Test Monitor

Monitors the MyRTA driving test booking page and sends a Pushover notification when timeslots become available.

## Setup

1. Install dependencies:
```bash
uv pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
python -m playwright install chromium
```

## Usage

Run the monitor:
```bash
python monitor.py
```

The script will:
- Check the booking page every 5 seconds
- Look for the absence of "There are no timeslots available for this week."
- Send you a Pushover notification when slots become available
- Stop automatically after finding slots

Press `Ctrl+C` to stop monitoring manually.

## Configuration

- Check interval: Edit `CHECK_INTERVAL` in `monitor.py` (default: 5 seconds)
- Pushover credentials: Configured in parent `.env` file
