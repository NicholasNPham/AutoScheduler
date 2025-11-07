# Working on connection to Notion API need to download notion api client

from datetime import timedelta, datetime, timezone



today = datetime.today() # YYYY-MM-DD HH:MM:SS.MMMMMM
num_of_today = today.weekday() # var set a num of day: e.g. monday = 0, tuesday = 1 ...

shift_dict = {}

for i in range(2, 7):
    today += timedelta(days=1)
    shift_dict["SAO10 SHIFT " + str(i - 1)] = [today.strftime("%Y-%m-%d") + "T08:00:00" + today.strftime("%z"), today.strftime("%Y-%m-%d") + "T17:00:00" + today.strftime("%z")]

for key, value in shift_dict.items():
    print(f"{key} : {value}")

# Need to fix for timezone we have daylight savings in florida. EST

# print(f"'{today}' variable type: {type(today)}")
# print(f"'{num_of_today}' variable type: {type(num_of_today)}")

