import time
from datetime import timedelta, datetime
import zoneinfo

last_run_day = None

while True:
    try:
        today = datetime.today().weekday()
        current_day = today
        print(today)

        if today == 5: # 5 Meaning Saturday
            if last_run_day != today:

                timezone = zoneinfo.ZoneInfo('America/New_York')
                today = datetime.now(timezone)  # YYYY-MM-DD HH:MM:SS.MMMMMM
                num_of_today = today.weekday()  # var set a num of day: e.g. monday = 0, tuesday = 1 ...

                shift_dict = {}

                today_ahead = today + timedelta(days=1)

                for i in range(2, 7):
                    today_ahead += timedelta(days=1)
                    start = today_ahead.strftime("%Y-%m-%d") + "T08:00:00" + today_ahead.strftime("%z")
                    end = today_ahead.strftime("%Y-%m-%d") + "T17:00:00" + today_ahead.strftime("%z")
                    shift_dict["SAO10 SHIFT " + str(i - 1)] = [start[1:22] + ":" + start[22:], end[1:22] + ":" + end[22:]]

                for key, value in shift_dict.items():
                    print(f"{key} : {value}")

                last_run_day = today # if it's the same day in 12 hours do not run
                print("AUTO POPULATED NOTION SCHEDULE")

        time.sleep(43200) # Check after 12 Hours
    except KeyboardInterrupt: # Keyboard Interruption
        print("Stopped")
        break # User Broke the Script
    except Exception as error:
        print(error)
        time.sleep(3600) # If Error Check Every 1 Hour