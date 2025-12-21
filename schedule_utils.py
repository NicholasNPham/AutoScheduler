"""
Schedule Utilities

Shared utility functions for generating and formatting schedules.
Used by work.py, task.py, and other schedule generation modules.

Author: Nicholas Pham
Last Modified: 2025-11-30
"""

# Standard Library Imports
from datetime import datetime, timedelta
import zoneinfo

# FUNCTIONS
def format_datetime_for_notion(dt):
    """
    Converts a datetime object to Notion's required ISO 8601 format.

    Notion API requires timezone offset with colon: YYYY-MM-DDTHH:MM:SS-05:00
    Python's strftime produces without colon: YYYY-MM-DDTHH:MM:SS-0500

    Args:
        dt: datetime object with timezone information

    Returns:
        str: ISO 8601 formatted string with proper timezone offset
    """
    formatted = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    formatted_with_colon = formatted[0:22] + ':' + formatted[22:]
    return formatted_with_colon

def get_current_time_in_timezone(timezone_name):
    """
    Get the current time in the specified timezone.

    Args:
        timezone_name: str - IANA timezone name (e.g., 'America/New_York')

    Returns:
        datetime: Current time in the specified timezone
    """
    timezone = zoneinfo.ZoneInfo(timezone_name)
    return datetime.now(timezone)

def should_run_today(current_weekday, trigger_day, last_run_day):
    """
    Determine if schedule generation should run today.

    Prevents duplicate runs by checking:
    1. Is today the trigger day (e.g., Saturday)?
    2. Have we NOT already run today?

    Args:
        current_weekday: int - Current day of week (0=Monday, 6=Sunday)
        trigger_day: int - Day of week to trigger on
        last_run_day: int or None - Last day we ran (None if never run)

    Returns:
        bool: True if schedule should be generated, False otherwise
    """
    if current_weekday == trigger_day and current_weekday != last_run_day:
        return True
    else:
        return False

def generate_shift_schedule(start_date, num_shifts, shift_start_hour, shift_end_hour, shift_prefix):
    """
    Generate a dictionary of shift schedules for consecutive days.

    Creates shifts starting from the day after start_date, each with
    specified start and end hours, formatted for Notion API.

    Args:
        start_date: datetime - Starting date (timezone-aware)
        num_shifts: int - Number of shifts to generate
        shift_start_hour: int - Hour when shift starts (0-23)
        shift_end_hour: int - Hour when shift ends (0-23)
        shift_prefix: str - Prefix for shift names (e.g., "SAO10 SHIFT")

    Returns:
        dict: Maps shift names to [start_time, end_time] lists
            Example: {"SAO10 SHIFT 1": ["2025-12-02T08:00:00-05:00", "2025-12-02T17:00:00-05:00"]}
    """

    shift_schedule_dictionary = {}
    current_date = start_date
    # Skips to Monday to iterate
    current_date += timedelta(days=2)

    for shift_number in range(1, num_shifts + 1):


        start_time = current_date.replace(hour=shift_start_hour, minute=0, second=0)
        end_time = current_date.replace(hour=shift_end_hour, minute=0, second=0)

        start_formatted = format_datetime_for_notion(start_time)
        end_formatted = format_datetime_for_notion(end_time)

        shift_name = f'{shift_prefix} {shift_number}'

        shift_schedule_dictionary[shift_name] = [start_formatted, end_formatted]

        current_date += timedelta(days=1)

    return shift_schedule_dictionary