import datetime
import time

"""
Well, fuck. This is going to be tough. For starters:
- use UTC everywhere
- example_time is how time is formatted in Influxdb

Let's use this as a chance to learn about time in Python
Use this module to parse time strings as needed.

More than you wanted to know about time formatting:
https://tools.ietf.org/html/rfc3339
"""

example_time = '2009-11-10T23:45:01.234567Z'
ts = time.strptime(example_time, '%Y-%m-%dT%H:%M:%S%z')

def strip_z(timestring) -> str:
    """Format for time.strptime to ingest"""
    return timestring.replace("Z","")
def add_z(timestring) -> str:
    """Convert to timestamp usable by Influxdb"""
    return timestring + "Z"

def parse_time(timestring) -> time.struct_time:
    """Return parsable time object"""
    try:
        return time.strptime(timestring, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        return time.strptime(add_z(timestring), '%Y-%m-%dT%H:%M:%S%z')
