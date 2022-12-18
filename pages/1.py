from datetime import datetime, timedelta
from time import strftime
print(datetime.datetime.now())
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+timedelta(days=1))
print(type(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

print(int(100/8))
