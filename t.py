
from datetime import datetime, timedelta

count=115

for m in range(20):
    last_login_time=datetime.utcnow() - timedelta(minutes = count)
    last_hour_date_time = datetime.utcnow() - timedelta(hours = 2)
    count+=1
    d = last_hour_date_time > last_login_time
    print(d)
    print(last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S'))