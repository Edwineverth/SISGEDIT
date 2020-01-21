import time
from datetime import datetime
import calendar
fp = time.strftime("%Y-%m-%d")
print(fp)
#fi = datetime.strptime('%m/%d/%Y')
#print(fi)
# print (datetime.date.today(fecha).isocalendar()[1])
#print(fi.strftime("%W"))


monthRange = calendar.monthrange(2019,5)
print(monthRange)
