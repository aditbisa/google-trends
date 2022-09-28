import logging
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from pytrends.request import TrendReq

from .calc import calculate

logger = logging.getLogger(__name__)


def collect(start_date: date, end_date: date, keywords: List[str], output_dir: Path):
    """
    Collect Google Trends and produce weekly, daily, and hourly data into csv files.
    """
    process_id = int(datetime.now().timestamp())
    call_count, hit_rate_limit = calculate(start_date, end_date)

    logger.info("Start collecting Google Trends data for:")
    logger.info(f"Start date: {start_date}")
    logger.info(f"End date: {end_date}")
    logger.info(f"Keywords: {keywords}")
    logger.info(f"Request count: {call_count}")
    logger.info(f"Hit rate limit: {hit_rate_limit}")
    logger.info(f"Output: {output_dir}/{process_id}_*")

    # Get hourly data from Google Trends
    # TODO: I got 400 & 500 from Google, need investigate!
    pytrends = TrendReq()

    # Info: the "date" is an index, not column.
    df_hourly: pd.DataFrame = pytrends.get_historical_interest(
        keywords,
        year_start=start_date.year,
        month_start=start_date.month,
        day_start=start_date.day,
        hour_start=0,
        year_end=end_date.year,
        month_end=end_date.month,
        day_end=end_date.day,
        hour_end=0,
    )
    logger.info("Collection is done, start processing")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Save hourly to csv
    hourly_csv = output_dir.joinpath(f"{process_id}_hourly.csv")
    df_hourly.to_csv(hourly_csv)

    # Calculate daily
    df_daily = df_hourly.resample("D").sum()

    # Save daily to csv
    daily_csv = output_dir.joinpath(f"{process_id}_daily.csv")
    df_daily.to_csv(daily_csv)

    # Calculate weekly
    df_weekly = df_hourly.resample("W").sum()

    # Save weekly to csv
    weekly_csv = output_dir.joinpath(f"{process_id}_weekly.csv")
    df_weekly.to_csv(weekly_csv)

    logger.info("Process completed")


def sanitize_command() -> Tuple:
    """
    Sanitize command arguments.

    Returns
    -------
    A tuple of arguments needed for `collect` method.
    """
    DATE_FORMAT = "%Y-%m-%d"
    TODAY_STRING = "today"

    if len(sys.argv) <= 3:
        print(f"Usage:\n  python {__file__} <start-date> <end-date | today> ...keywords")
        print(f"Example:\n  python {__file__} 2015-01-01 today bitcoin dogecoin")
        exit(1)

    start_date_str = sys.argv[1]
    end_date_str = TODAY_STRING if len(sys.argv) < 3 else sys.argv[2]
    keywords = sys.argv[3:]

    try:
        start_date = datetime.strptime(start_date_str, DATE_FORMAT).date()
        if end_date_str == TODAY_STRING:
            end_date = datetime.now().date()
        else:
            end_date = datetime.strptime(end_date_str, DATE_FORMAT).date()
    except:
        print(f"Date format is incorrect.")
        exit(1)

    return start_date, end_date, keywords


if __name__ == "__main__":
    # Suppress pandas FutureWarning produced by pytrends. AAARGHHHHHH 😱
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Print log to terminal
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    args = sanitize_command()
    output_dir = Path(os.getcwd()).joinpath("output")
    collect(*args, output_dir)
