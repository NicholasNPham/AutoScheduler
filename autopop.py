import time
from datetime import datetime

last_run_day = None

while True:
    try:
        today = datetime.today().weekday()
        current_day = today
        print(today)

        if today == 5: # 5 Meaning Saturday
            if last_run_day != today:
                pass

                # API NOTION CALL

                last_run_day = today # if it's the same day in 12 hours do not run
                print("AUTO POPULATED NOTION SCHEDULE")

        time.sleep(43200) # Check after 12 Hours
    except KeyboardInterrupt: # Keyboard Interruption
        print("Stopped")
        break # User Broke the Script
    except Exception as error:
        print(error)
        time.sleep(3600) # If Error Check Every 1 Hour