import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# Body Fat Percentage and Weight Over Time (3D)
x = ['2025-11-27','2025-12-31','2026-02-05','2026-02-24','2026-03-13','2026-03-26','2026-04-06','2026-04-17','2026-05-04','2026-05-14']
y = [22.9,26.1,23.1,24.0,26.1,26.3,25.4,26.6,26.1,26.2]
z = [69,69,66,70,72,73,74,73,75,72]

dates = [datetime.strptime(date, '%Y-%m-%d') for date in x]
date_nums = mdates.date2num(dates)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(date_nums, y, z, marker='o')
ax.set_ylabel('BodyFat(%)')
ax.set_zlabel('Weight(kg)')
ax.set_title('Inbody Results Over Time (3D)')

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
fig.autofmt_xdate()

plt.show()
