import pytz
import time
import datetime
print(time.strftime("%a, %d %b %Y %H:%M:%S %Z %z", time.gmtime()))
print(time.strftime("%a, %d %b %Y %H:%M:%S %Z %z", time.localtime()))

# //require a 2 letter country code


def GetTimeZoneName(timezone, country_code):

    # see if it's already a valid time zone name
    if timezone in pytz.all_timezones:
        return timezone

    # if it's a number value, then use the Etc/GMT code
    try:
        offset = int(timezone)
        if offset > 0:
            offset = '+' + str(offset)
        else:
            offset = str(offset)
        return 'Etc/GMT' + offset
    except ValueError:
        pass

    # look up the abbreviation
    country_tzones = None
    try:
        country_tzones = pytz.country_timezones[country_code]
    except:
        pass
    set_zones = set()
    if country_tzones is not None and len(country_tzones) > 0:
        for name in country_tzones:
            tzone = pytz.timezone(name)
            for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, datetime.datetime.now(tzone).tzname()]]):
                if tzabbrev.upper() == timezone.upper():
                    set_zones.add(name)
        if len(set_zones) > 0:
            return min(set_zones, key=len)

        # none matched, at least pick one in the right country
        return min(country_tzones, key=len)

    # invalid country, just try to match the timezone abbreviation to any time zone
    for name in pytz.all_timezones:
        tzone = pytz.timezone(name)
        for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info', [[None, None, datetime.datetime.now(tzone).tzname()]]):
            if tzabbrev.upper() == timezone.upper():
                set_zones.add(name)

    if len(set_zones) > 0:
        return min(set_zones, key=len)
    return -1


entered_date = '2020-04-18'
entered_time = '12:46:00'
# gets string futher convert to time zone object
t1 = GetTimeZoneName('XXX', 'CN')
datetime_unaware = datetime.datetime(*map(int, entered_date.split('-')), *map(int, entered_time.split(':')))
datetime_aware = pytz.timezone(t1).localize(datetime_unaware)
# print(datetime_aware - datetime.datetime.now()) error
# print(datetime_aware, datetime_aware.astimezone(pytz.utc))
# print(datetime_aware.strftime("% a, % d % b % Y % H: % M: % S % Z % z"))

# print(GetTimeZoneName('edt', ''))
# t1 = GetTimeZoneName('usa', 'IN')  # further convert to tzone object
# t2 = GetTimeZoneName('edt', 'us')
# utc_now = datetime.datetime.now(pytz.utc)
# print(t1, t2)
# t1 = utc_now.astimezone(pytz.timezone(t1))
# t2 = utc_now.astimezone(pytz.timezone(t2))
# # aware time zone object
# print(t1, t2)
# print(t2 - t1)
