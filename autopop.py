import time
from datetime import datetime

while True:
    try:
        today = datetime.today().weekday()
        print(today)
        if today == 5: # 5 Meaning Saturday
            pass
            # This is where the Notion API Logic Goes

        time.sleep(43200)
    except KeyboardInterrupt:
        print("Stopped")
        break
    except Exception as error:
        print(error)
        time.sleep(3600)