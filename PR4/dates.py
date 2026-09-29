from datetime import datetime, timedelta

now = datetime.now()
five = now - timedelta(days=5)

print("Today:", now.strftime("%Y-%m-%d"))
print("5 days", five.strftime("%Y-%m-%d"))