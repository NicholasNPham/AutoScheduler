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

