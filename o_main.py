"""
Notion Schedule Auto-Populator

Automatically generates and uploads weekly shift schedules to a Notion database.
Runs every Saturday to create Monday-Friday shifts for the following week.
"""

"""IMPORTS"""

# Standard Library Imports
import time
from datetime import timedelta, datetime
import zoneinfo

# Third-party imports
from notion_client import Client

"""CONSTANTS"""

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
def format_datetime_for_notion(dt):
    formatted = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    formatted_with_colon = formatted[0:22] + ':' + formatted[22:]
    return formatted_with_colon

def get_current_time_in_timezone(timezone_name):
    timezone = zoneinfo.ZoneInfo(timezone_name)
    return datetime.now(timezone)

# MAIN LOOP SETUP

# MAIN LOOP