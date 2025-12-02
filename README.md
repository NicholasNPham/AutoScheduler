# Notion Schedule Auto-Populator

Automated scheduling system that generates and uploads weekly shift schedules to Notion databases. Built following NASA coding standards for maintainability, modularity, and clarity.

## Author
Nicholas Pham  
Last Modified: 2025-12-01

---

## Overview

This system automatically generates weekly work schedules every Saturday and updates them to a Notion database. It runs continuously in the background, checking every 12 hours for the trigger day.

**Current Features:**
- Generates Monday-Friday work shifts (8 AM - 5 PM EST)
- Automatically updates Notion database
- Prevents duplicate runs on the same day
- Handles errors gracefully with retry logic
- Extensible architecture for adding task schedules

---

## Architecture

The system is divided into four modular components:

### 1. `schedule_utils.py` - Shared Utilities
Reusable date/time functions used across all schedule types.

**Functions:**
- `format_datetime_for_notion(dt)` - Converts datetime to Notion's ISO 8601 format
- `get_current_time_in_timezone(timezone_name)` - Gets current time in specified timezone
- `should_run_today(current_weekday, trigger_day, last_run_day)` - Determines if schedule should run
- `generate_shift_schedule(...)` - Generates shift dictionary for multiple days

### 2. `work.py` - Work Schedule Configuration
Work-specific constants and schedule generation.

**Constants:**
- Day of week definitions (MONDAY=0 through SUNDAY=6)
- Trigger day: `SATURDAY` (when to generate schedules)
- Shift timing: 8 AM - 5 PM
- Number of shifts: 5 (Monday-Friday)
- Timezone: America/New_York
- Shift prefix: "SAO10 SHIFT"

**Functions:**
- `generate_work_schedule(current_time)` - Generates work shifts using work-specific settings

### 3. `notion.py` - Notion API Wrapper
Handles all Notion database operations.

**Functions:**
- `initialize_notion_client(api_token)` - Creates authenticated Notion client
- `get_database_row_ids(client, database_id)` - Retrieves all row IDs from database
- `fix_row_order(row_ids)` - Applies workaround for known row ordering bug
- `create_notion_properties(shift_name, start_time, end_time)` - Builds property dictionary
- `update_notion_row(...)` - Updates single database row
- `update_database_with_schedule(...)` - Updates entire database with schedule

### 4. `scheduler.py` - Main Coordinator
Entry point that runs the continuous scheduling loop.

**Functionality:**
- Initializes Notion client at startup
- Checks every 12 hours if it's the trigger day
- Generates and uploads schedules when triggered
- Handles keyboard interrupts (Ctrl+C) gracefully
- Retries on errors with 1-hour delay

---

## File Structure

```
.
├── scheduler.py          # Main entry point - run this
├── schedule_utils.py     # Shared date/time utilities
├── work.py              # Work schedule configuration
├── notion.py            # Notion API wrapper
├── key.py               # API credentials (not in repo)
└── README.md            # This file
```

---

## Requirements

### Python Version
- Python 3.9+ (requires `zoneinfo` from standard library)

### Dependencies
```
notion-client==2.4.0
```

Install with:
```bash
pip install notion-client==2.4.0
```

### API Credentials
Create a `key.py` file with your Notion credentials:

```python
# Notion API credentials
SECRET = "your_notion_integration_token"
WORK_PAGE_ID = "your_work_database_id"
TASK_PAGE_ID = "your_task_database_id"  # For future use
```

**How to get credentials:**
1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the "Internal Integration Token" → this is your `SECRET`
4. Share your database with the integration
5. Get the database ID from the URL → this is your `WORK_PAGE_ID`

---

## Usage

### Running the Scheduler

```bash
python scheduler.py
```

**Output:**
```
Initializing Notion Client...
Client created Successfully...
Scheduler started!
Checking every 12 hours for trigger day (Saturday)

Checking... Day: 1, Time: 2025-12-01 14:30:00
```

### Stopping the Scheduler

Press `Ctrl+C` to stop gracefully:
```
Scheduler stopped by user.
```

---

## Configuration

### Changing Schedule Settings

Edit constants in `work.py`:

```python
# Change trigger day
TRIGGER_DAY = SATURDAY  # Change to any day (0-6)

# Change shift times
SHIFT_START_HOUR = 8   # 8 AM
SHIFT_END_HOUR = 17    # 5 PM

# Change number of shifts
NUMBER_OF_SHIFTS = 5   # Monday-Friday

# Change check interval
HOURS_BETWEEN_CHECKS = 12  # Check every 12 hours
```

### Changing Timezone

```python
TIMEZONE_NAME = 'America/New_York'  # Change to your timezone
```

Find valid timezone names: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

---

## How It Works

### Schedule Generation Flow

1. **Saturday Morning** - Scheduler detects it's the trigger day
2. **Generate Schedule** - Creates 5 shifts (Monday-Friday) starting the next day
3. **Format Dates** - Converts to Notion's required ISO 8601 format
4. **Query Database** - Gets row IDs from Notion database
5. **Fix Order** - Applies workaround for rows 2 and 3 being swapped
6. **Update Rows** - Updates each row with shift information
7. **Sleep** - Waits 12 hours before checking again

### Duplicate Prevention

The system tracks `last_run_day` to prevent running multiple times on the same day. Even if you restart the script on Saturday, it won't regenerate the schedule until the next Saturday.

### Error Handling

- **Keyboard Interrupt**: Stops gracefully
- **API Errors**: Logs error and retries in 1 hour
- **Connection Issues**: Automatically retries with exponential backoff (handled by notion-client)

---

## Extending the System

### Adding Task Schedules

1. **Create `task.py`** (similar to `work.py`):
```python
TRIGGER_DAY = SUNDAY  # Different trigger day
TASK_PREFIX = "TASK"
# ... other task-specific constants
```

2. **Update `scheduler.py`** to check both work and tasks:
```python
from task import generate_task_schedule, TASK_TRIGGER_DAY

# In run_scheduler():
if should_run_today(current_weekday, TRIGGER_DAY, last_work_run):
    # Generate work schedule
    
if should_run_today(current_weekday, TASK_TRIGGER_DAY, last_task_run):
    # Generate task schedule
```

---

## Troubleshooting

### "Client created Successfully..." but nothing happens
- The scheduler is waiting for Saturday (trigger day)
- Check current day with: `datetime.now().weekday()` (0=Monday, 5=Saturday)

### "Error: Schedule has 5 shifts but database only has 3 rows"
- Your Notion database doesn't have enough rows
- Add more rows to the database or reduce `NUMBER_OF_SHIFTS`

### "Applied row order correction (swapped rows 2 and 3)"
- This is normal - it's a known Notion API quirk
- The fix ensures shifts go to the correct rows

### Authentication Errors
- Verify `SECRET` in `key.py` is correct
- Ensure database is shared with the integration
- Check that `WORK_PAGE_ID` matches your database ID

---

## Code Quality Standards

This project follows **NASA coding standards**:

✅ **Self-documenting code** - Clear variable and function names  
✅ **No magic numbers** - All constants defined at the top  
✅ **Single-purpose functions** - Each function does one thing  
✅ **Comprehensive docstrings** - Every function documented  
✅ **Error handling** - Specific exception handling  
✅ **Modular architecture** - Separation of concerns  
✅ **Type clarity** - Clear parameter and return types  

---

## Future Enhancements

- [ ] Add task schedule generation (`task.py`)
- [ ] Web dashboard for viewing schedules
- [ ] Email notifications when schedules are generated
- [ ] Multiple database support
- [ ] Configurable shift patterns (not just 8-5)
- [ ] Holiday awareness (skip scheduling on holidays)
- [ ] Logging to file for debugging

---

## License

Personal project - for educational and personal use.

---

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify your `key.py` credentials
3. Check Notion API status: https://status.notion.so/
4. Review function docstrings for parameter details

---

## Changelog

### Version 1.0.0 (2025-12-01)
- Initial release
- Work schedule automation
- Notion integration
- NASA-standard refactoring complete