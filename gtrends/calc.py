import math
import sys
from datetime import datetime, timedelta
from typing import Tuple


def calculate(start_date: datetime.date, end_date: datetime.date) -> Tuple[int, bool]:
    """
    Calculate Google Trends request call count for hourly data and determine if its hits rate limit.
    """
    RATE_LIMIT = 1400
    HOURS_PER_CALL = 7 * 24

    time_delta: timedelta = end_date - start_date
    hours = time_delta.total_seconds() / 3600
    call_count = math.ceil(hours / HOURS_PER_CALL)
    hit_rate_limit = call_count >= RATE_LIMIT

    return call_count, hit_rate_limit


def sanitize_command() -> Tuple:
    """
    Sanitize command arguments.

    Returns
    -------
    A tuple of arguments needed for `calculate` method.
    """
    DATE_FORMAT = "%Y-%m-%d"
    TODAY_STRING = "today"

    if len(sys.argv) <= 1:
        print(f"Usage:\n  python {__file__} <start-date> <end-date, default: today>")
        print(f"Example:\n  python {__file__} 2015-01-01 2018-01-01")
        exit(1)

    start_date_str = sys.argv[1]
    end_date_str = TODAY_STRING if len(sys.argv) < 3 else sys.argv[2]

    try:
        start_date = datetime.strptime(start_date_str, DATE_FORMAT).date()
        if end_date_str == TODAY_STRING:
            end_date = datetime.now().date()
        else:
            end_date = datetime.strptime(end_date_str, DATE_FORMAT).date()
    except:
        print(f"Date format is incorrect.")
        exit(1)

    return start_date, end_date


if __name__ == "__main__":
    args = sanitize_command()
    call_count, hit_rate_limit = calculate(*args)
    print(f"Call count: {call_count}")
    print(f"Hit rate limit: {hit_rate_limit}")
