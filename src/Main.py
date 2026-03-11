from NepaliDate import NepaliDate
from datetime import datetime

dt = datetime(2023, 3, 11)
nd = NepaliDate(dt)
print(nd.format("YYYY MM DD"))
