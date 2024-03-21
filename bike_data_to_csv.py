import pandas as pd
import os

folder_path = './bike-data'
for filename in os.listdir(folder_path):

    df = pd.read_csv(os.path.join(folder_path, filename))

    df['month'] = pd.to_datetime(df['started_at']).dt.month
    df['year'] = pd.to_datetime(df['started_at']).dt.year

    monthly_counts = df.groupby(['start_station_id', 'year', 'month']).size().reset_index(name='count')
    result = monthly_counts.groupby(['start_station_id', 'month'])['count'].mean().reset_index(name='average_per_month')
    result = pd.merge(result, df[['start_station_id', 'start_lng', 'start_lat']], on='start_station_id', how='left').drop_duplicates()
    result = result.groupby(['start_station_id', 'month']).first().reset_index().drop_duplicates()

    file_exists = os.path.isfile('average_per_month.csv')
    result.to_csv('bike_data.csv', mode='a', header=(not file_exists), index=False)