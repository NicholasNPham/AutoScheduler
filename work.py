"""
Work Schedule Generator

Generates weekly work shift schedules for SAO10 shifts.
Runs on Saturdays to create Monday-Friday schedules (8 AM - 5 PM EST).

This module contains work-specific constants and configuration.
Schedule generation utilities are imported from schedule_utils.py.
Notion database operations are handled by notion.py.

Author: Nicholas Pham
Last Modified: 2025-11-30
"""

# Standard Library Imports
import time

# Local Imports
from schedule_utils import (
    format_datetime_for_notion,
    get_current_time_in_timezone,
    should_run_today,
    generate_shift_schedule
)

# CONSTANTS

# Days of the Week
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

# Schedule Settings
TRIGGER_DAY = SATURDAY
NUMBER_OF_SHIFTS = 5

# Time-Related Constants
SECONDS_PER_HOUR = 3600
HOURS_BETWEEN_CHECKS = 12
CHECK_INTERVAL_SECONDS = HOURS_BETWEEN_CHECKS * SECONDS_PER_HOUR # Calculates 43200 seconds

ERROR_RETRY_HOURS = 1
ERROR_RETRY_SECONDS = ERROR_RETRY_HOURS * SECONDS_PER_HOUR # 3600

# Shift Timing
SHIFT_START_HOUR = 8 # 8:00AM
SHIFT_END_HOUR = 17  # 5:00PM (17:00) in 24-H Format

# Other settings
TIMEZONE_NAME = 'America/New_York'
SHIFT_NAME_PREFIX = 'SAO10 SHIFT'

# FUNCTIONS
def generate_work_schedule(current_time):
    """
    Generate work shift schedule using work-specific settings.

    Args:
        current_time: datetime - Current time (timezone-aware)

    Returns:
        dict: Work shift schedule for the week
    """
    return generate_shift_schedule(
        start_date=current_time,
        num_shifts=NUMBER_OF_SHIFTS,
        shift_start_hour=SHIFT_START_HOUR,
        shift_end_hour=SHIFT_END_HOUR,
        shift_prefix=SHIFT_NAME_PREFIX
    )