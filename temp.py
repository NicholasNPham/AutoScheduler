# Working on connection to Notion API need to download notion api client

from datetime import timedelta, datetime
import zoneinfo

timezone = zoneinfo.ZoneInfo('America/New_York')
today = datetime.now(timezone) # YYYY-MM-DD HH:MM:SS.MMMMMM
num_of_today = today.weekday() # var set a num of day: e.g. monday = 0, tuesday = 1 ...

shift_dict = {}

today_ahead = today + timedelta(days=1)

for i in range(2, 7):
    today_ahead += timedelta(days=1)
    start = today_ahead.strftime("%Y-%m-%d") + "T08:00:00" + today_ahead.strftime("%z")
    end = today_ahead.strftime("%Y-%m-%d") + "T17:00:00" + today_ahead.strftime("%z")
    shift_dict["SAO10 SHIFT " + str(i - 1)] = [start[1:22] + ":" + start[22:], end[1:22] + ":" + end[22:]]

for key, value in shift_dict.items():
    print(f"{key} : {value}")

# print(f"'{today}' variable type: {type(today)}")
# print(f"'{num_of_today}' variable type: {type(num_of_today)}")

