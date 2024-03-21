import pandas as pd
import json



df = pd.read_csv('monthly_stop_data.csv')

df['month'] = pd.to_datetime(df['Month_Beginning']).dt.month
df['year'] = pd.to_datetime(df['Month_Beginning']).dt.year

df['MonthTotal'] = pd.to_numeric(df['MonthTotal'])
max_MonthTotal = df['MonthTotal'].max()
df['heat'] = (df['MonthTotal'] / max_MonthTotal).round(2)
df = df[df['year'] == 2018]

# csv_file = 'bike_data_heat.csv'
# df.to_csv(csv_file, index=False)
# df = pd.read_csv(csv_file)

for month in range(1, 13):
    df_month = df[df['month'] == month]

    df_selected = df_month[['LONGITUDE', 'LATITUDE', 'heat']]

    json_array = df_selected.to_dict(orient='records')

    output_file = "output" + str(month) + ".json"
    with open(output_file, 'w') as f:
        json.dump(json_array, f, indent=4)