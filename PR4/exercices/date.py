from datetime import datetime, timedelta

current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print("1. Subtract 5 days:")
print("Current Date:", current_date.strftime("%Y-%m-%d"))
print("5 Days Ago:  ", five_days_ago.strftime("%Y-%m-%d"))


today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("2. Yesterday, Today, Tomorrow:")
print("Yesterday:", yesterday)
print("Today:    ", today)
print("Tomorrow: ", tomorrow)

now = datetime.now()
without_microseconds = now.replace(microsecond=0)
print("3. Drop microseconds:")
print("Original Datetime:", now)
print("Without Microsec: ", without_microseconds)

date1 = datetime(2026, 9, 28, 10, 0, 0)
date2 = datetime(2026, 9, 28, 12, 30, 0)
difference_in_seconds = (date2 - date1).total_seconds()
print("4. Difference in seconds:")
print(f"Difference between {date1} and {date2}: {difference_in_seconds} seconds")