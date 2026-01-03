"""
Schedule Coordinator

Main scheduler that coordinates schedule generation and Notion database updates.
Runs continuously, checking every 12 hours for scheduled tasks.

Currently manages:
    - Work schedules: Runs on Saturdays to generate Monday-Friday shifts
    - (Future) Task schedules: Will be added later

This is the entry point for the automated scheduling system. It coordinates
between schedule generation modules (work.py, task.py) and the Notion API
wrapper (notion.py) to keep schedules up-to-date.

Usage:
    python scheduler.py

Requirements:
    - All local modules: schedule_utils, work, notion, key
    - Notion API credentials configured in key.py

Author: Nicholas Pham
Last Modified: 2025-12-01
"""
# Standard Imports
import time

# Local Imports
from key import SECRET, WORK_PAGE_ID, TASK_PAGE_ID
from work import (
    TRIGGER_DAY,
    TIMEZONE_NAME,
    CHECK_INTERVAL_SECONDS,
    ERROR_RETRY_SECONDS,
    generate_work_schedule
)
from notion import (
    initialize_notion_client,
    update_database_with_schedule
)
from schedule_utils import (
    get_current_time_in_timezone,
    should_run_today
)

# MAIN LOOP
def run_scheduler():
    """
    Main scheduler loop - runs continuously and coordinates schedule updates.

    [Add more details about what it does]
    """
    print("Initializing Notion Client...")
    client = initialize_notion_client(SECRET)

    print(f"Scheduler started!")
    print(f"Checking every {CHECK_INTERVAL_SECONDS // 3600} hours for trigger day (Saturday)\n")

    last_run_day = None
    while True:
        try:
            current_time = get_current_time_in_timezone(TIMEZONE_NAME)
            current_weekday = current_time.weekday()

            print(f"Checking... Day: {current_weekday}, Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}, Last Check Date: {last_run_day}")

            if should_run_today(current_weekday, TRIGGER_DAY, last_run_day):
                print(">>> GENERATING WORK SCHEDULE <<<")
                schedule = generate_work_schedule(current_time)

                print("Updating Notion database...")
                update_database_with_schedule(client, WORK_PAGE_ID, schedule)

            last_run_day = current_weekday
            print("✓ Schedule update complete!\n")

            time.sleep(CHECK_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n\nScheduler stopped by user.")
            break
        except Exception as error:
            print(error)
            time.sleep(ERROR_RETRY_SECONDS)

if __name__ == "__main__":
    run_scheduler()