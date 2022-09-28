# Google Trends Data Collection

This project will collect Google Trends and produce weekly, daily, and hourly data into csv files.


## Be aware of Google rate limit

Based on the documentation of [pytrends](https://github.com/GeneralMills/pytrends#caveats), an unofficial API for Google Trends that we use in this project, Google will rate limit your request after 1,400 sequential requests of a 4 hours timeframe.

Calculate your requests call count with this command:
```
./main.sh calc <start-date> <stop-date, default: today>
./main.sh calc 2015-01-01 2018-01-01
./main.sh calc 2015-01-01 today
./main.sh calc 2015-01-01
```
