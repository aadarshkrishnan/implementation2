import pandas as pd
import json

csv_file = 'bike_data_heat.csv'

df = pd.read_csv(csv_file)

for month in range(1, 13):
    df_month = df[df['month'] == month]

    df_selected = df_month[['start_lng', 'start_lat', 'heat']]

    json_array = df_selected.to_dict(orient='records')

    output_file = "output" + str(month) + ".json"
    with open(output_file, 'w') as f:
        json.dump(json_array, f, indent=4)