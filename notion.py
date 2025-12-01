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
