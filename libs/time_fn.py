# http://docs.python.org/3.3/library/time.html
# http://docs.python.org/3.3/library/calendar.html#calendar.timegm

import time, calendar, datetime

# Time is to be stored in seconds since the epoch
def epoch_time():
    "returns time in seconds since the epoch"
    return time.time()

def UTC_time():
    "returns time in UTC form"
    return time.gmtime(epoch_time())
    
def UTC_to_epoch(UTC):
    "converts a structured time to epoch time"
    return calendar.timegm(UTC)

def epoch_to_UTC(S):
    "converts epoch time to UTC"
    return time.gmtime(S)

def T_to_epoch(T):
    "converts local time to epoch time"
    return time.mktime(T)

def epoch_to_T(S):
    return time.localtime(S)

def UTC_to_T(UTC):
    return epoch_to_T(UTC_to_epoch(UTC))

def T_to_UTC(T):
    return epoch_to_UTC(T_to_epoch(T))
