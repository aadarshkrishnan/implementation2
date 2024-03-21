import pandas as pd

df = pd.read_csv('bike_data.csv')

df['average_per_month'] = pd.to_numeric(df['average_per_month'])

max_average_per_month = df['average_per_month'].max()

df['heat'] = (df['average_per_month'] / max_average_per_month).round(2)

df.to_csv('bike_data_heat.csv', index=False)