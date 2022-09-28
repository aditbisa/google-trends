# Google Trends Data Collection

This project will collect Google Trends and produce weekly, daily, and hourly data into csv files.


## Setup

Install packages:
```
poetry install
-or-
pip install - requirements.txt
```


## Usage

Run command:
```
Format:
./main.sh collect <start-date> <end-date | today> ...keywords

Examples:
./main.sh collect 2020-01-01 2022-01-01 bitcoin
./main.sh collect 2015-01-01 today bitcoin dogecoin
```


## Be aware of Google rate limit

Based on the documentation of [pytrends](https://github.com/GeneralMills/pytrends#caveats), an unofficial API for Google Trends that we use in this project, Google will rate limit your request after 1,400 sequential requests of a 4 hours timeframe.

Calculate your requests call count with this command:
```
Format:
./main.sh calc <start-date> <end-date, default: today>

Examples:
./main.sh calc 2015-01-01 2018-01-01
./main.sh calc 2015-01-01 today
./main.sh calc 2015-01-01
```


## TODO
- Correction to `collect` usage by calling the module.
- Add timestamp to log running time.
- Investigate and handle request failure from Google. I got 400 & 500 response code.
- Use proxies for heavy load.
- Parallel process to speed up the collection.
