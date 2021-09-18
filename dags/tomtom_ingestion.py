import requests
import argparse
import os

from datetime import timedelta, datetime
import pandas as pd
import json

import config

rename_header = { 'JamsDelay'          : 'jams_delay', 
                  'TrafficIndexLive'   : 'traffic_index', 
                  'UpdateTime'         : 'date_time', 
                  'JamsLength'         : 'jams_length', 
                  'JamsCount'          : 'jams_count', 
                  'TrafficIndexWeekAgo': 'traffic_index_weekago'}
reposition_header = ['timestamp', 'date_time', 'traffic_index', 'jams_count', 'jams_length', 'jams_delay', 'traffic_index_weekago']

def get_yesterday_date(fetch_date):
    return datetime.strptime(fetch_date, '%Y-%m-%d').date() - timedelta(1)

def get_file_path(fetch_date):
    yesterday = get_yesterday_date(fetch_date)
    filename = "tomtom_{}.csv".format(yesterday)
    return os.path.join(config.CSV_FILE_DIR, filename)

def import_data():
    url = config.TOMTOM_API
    data_req = requests.get(url)
    data_json = data_req.json()
    return data_json

def transform_data(data_json):
    dataframe = pd.DataFrame(data_json['data'])
    df = dataframe.rename(columns = rename_header)
    df['timestamp'] = df['date_time'].copy()
    df = df[reposition_header]
    # convert timezone(UTC) to local time(Jakarta)
    df.date_time = pd.to_datetime(df.date_time, unit="ms")
    df.date_time = df.date_time.dt.tz_localize('UTC').dt.tz_convert('Asia/Jakarta').apply(lambda d: d.replace(tzinfo=None))
    df['weekday'] = df['date_time'].dt.day_name()
    df['timestamp'] = df['timestamp']/1000
    df['timestamp'] = df['timestamp'].astype(int)
    df = df.fillna(0)
    df['traffic_index_weekago'] = df['traffic_index_weekago'].astype(int)
    return df

def get_new_data(df, fetch_date):
    yesterday = get_yesterday_date(fetch_date)
    df = df.sort_values(by=['timestamp'], ascending=True)
    data_to_append = df[(df['date_time'].dt.date == yesterday)]
    return data_to_append

def save_new_data_to_csv(data_to_append, fetch_date):
    filename = get_file_path(fetch_date)
    if not data_to_append.empty:
        data_to_append.to_csv(filename, encoding='utf-8', index=False)

def main(fetch_date):
    data_json = import_data()
    df = transform_data(data_json)
    data_to_append = get_new_data(df, fetch_date)
    save_new_data_to_csv(data_to_append, fetch_date)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, type=str)
    args = parser.parse_args()
    main(args.date)