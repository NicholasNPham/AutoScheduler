"""
Notion Database Operations

Handles all interactions with the Notion API for schedule management.
Provides functions to initialize the client, query databases, and update
shift schedules in Notion database rows.

This module abstracts Notion-specific operations so that work.py and task.py
can update their schedules without dealing with API details.

Key Operations:
    - Initialize Notion client with API credentials
    - Query database to retrieve row IDs
    - Update database rows with formatted schedule data
    - Handle known Notion API quirks (e.g., row ordering issues)

Requirements:
    - notion_client==2.4.0
    - API token and database ID stored in key.py

Author: Nicholas Pham
Last Modified: 2025-11-30
"""

# Third-party Imports
from notion_client import Client

# Local Imports
from key import * # Notion API credentials

# CONSTANTS

# Notion Database Property Names
NOTION_NAME_PROPERTY = "Name"
NOTION_DATE_PROPERTY = "Date"

# FUNCTIONS

def initialize_notion_client(api_token):
    """
    Initialize Notion client with API credentials.

    Args:
        api_token: str - Notion integration API token

    Returns:
        Client: Initialized Notion client object
    """
    notion = Client(auth=api_token)
    print("Client created Successfully...")
    return notion


def get_database_row_ids(client, database_id):
    """
       Query Notion database and return list of row IDs.

       Args:
           client: Client - Initialized Notion client
           database_id: str - ID of the Notion database to query

       Returns:
           list: List of row IDs (page IDs) from the database
    """
    row_id_list = []

    response = client.databases.query(database_id=database_id)

    for page in response['results']:
        row_id = page['id']
        row_id_list.append(row_id)

    print(f'Found {len(row_id_list)} row IDs')

    return row_id_list


def fix_row_order(row_ids):
    """
    Apply known row ordering fix to Notion database results.

    NOTE: This is a workaround for a known issue where rows 2 and 3
    are returned in the wrong order from the Notion API.

    Args:
        row_ids: list - List of row IDs from database

    Returns:
        list: Row IDs with corrections applied
    """
    if len(row_ids) >= 3:
        row_ids[1], row_ids[2] = row_ids[2], row_ids[1]
        print("Applied row order correction (swapped rows 2 and 3)")

    return row_ids

def create_notion_properties(shift_name, start_time, end_time):
    """
    Create a Notion properties dictionary for a shift.

    Args:
        shift_name: str - Name of the shift (e.g., "SAO10 SHIFT 1")
        start_time: str - ISO 8601 formatted start time
        end_time: str - ISO 8601 formatted end time

    Returns:
        dict: Notion API properties object ready for page update
    """
    text_property = {"title": [{"text": {"content": shift_name}}]}
    date_property = {"date": {"start": start_time, "end": end_time}}
    return {NOTION_NAME_PROPERTY: text_property, NOTION_DATE_PROPERTY: date_property}

def update_notion_row(client, row_id, shift_name, start_time, end_time):
    """
    Update a single row in the Notion database with shift information.

    Args:
        client: Client - Initialized Notion client
        row_id: str - ID of the row (page) to update
        shift_name: str - Name of the shift
        start_time: str - ISO 8601 formatted start time
        end_time: str - ISO 8601 formatted end time

    Returns:
        bool: True if update successful, False otherwise
    """
    properties = create_notion_properties(shift_name, start_time, end_time)
    try:
        client.pages.update(page_id=row_id, properties=properties)
        print(f"✓ Updated: {shift_name}")
        return True
    except Exception as e:
        print(f"✗ Failed to update {shift_name}: {type(e).__name__} - {e}")
        return False

def update_database_with_schedule(client, database_id, schedule):
    """
    Update Notion database with a complete shift schedule.

    Args:
        client: Client - Initialized Notion client
        database_id: str - ID of the Notion database
        schedule: dict - Maps shift names to [start_time, end_time] lists
                        Example: {"SAO10 SHIFT 1": ["2025-12-02T08:00:00-05:00", "2025-12-02T17:00:00-05:00"]}

    Returns:
        int: Number of rows successfully updated
    """
    rows = get_database_row_ids(client, database_id)
    rows = fix_row_order(rows)
    if len(schedule) > len(rows):
        print(f"✗ Error: Schedule has {len(schedule)} shifts but database only has {len(rows)} rows")
        return 0
    else:

        successful_updates = 0

        for index, (shift_name, times) in enumerate(schedule.items()):
            start_time = times[0]
            end_time = times[1]

            if update_notion_row(client, rows[index], shift_name, start_time, end_time):
                successful_updates += 1

    print(f"✓ Updated {successful_updates}/{len(schedule)} rows successfully")
    return successful_updates