import pytz
import datetime
local_tz = pytz.timezone('America/Halifax') # use your local timezone name here
# NOTE: pytz.reference.LocalTimezone() would produce wrong result here

## You could use `tzlocal` module to get local timezone on Unix and Win32
# from tzlocal import get_localzone # $ pip install tzlocal

# # get local timezone
# local_tz = get_localzone()

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

print(aslocaltimestr(datetime(2010,  6, 6, 17, 29, 7, 730000)))
print(aslocaltimestr(datetime(2010, 12, 6, 17, 29, 7, 730000)))
print(aslocaltimestr(datetime.utcnow()))