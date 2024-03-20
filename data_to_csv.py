import pandas as pd
import os
from datetime import datetime

bus_numbers_file = "cta/cta-ridership-bus-routes-monthly-day-type-averages-totals.csv"

bus_route_info_file = "cta/cta-system-information-bus-stop-locations-in-digital-sign-project.csv"

# bicycle_trip_directory = "bicycle"

# df=pd.DataFrame()
# df_chunk=pd.DataFrame()
# for filename in os.listdir(bicycle_trip_directory):
#     filepath = os.path.join(bicycle_trip_directory, filename)
#     if os.path.isfile(filepath):
#         print(filepath)
        
#         current = pd.read_csv(filepath)
#         for i, row in current.iterrows():
#             month_beginning = row['ended_at']
#             month_beginning = datetime.strptime(month_beginning, '%Y-%m-%d %H:%M:%S')
#             month_beginning = month_beginning.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#             month_beginning = str(month_beginning.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
#             new_row = pd.DataFrame({'ride_id': [row['ride_id']],
#                                 'start_lat': [row['start_lat']],
#                                 'start_lng': [row['start_lng']],
#                                 'end_lat': [row['end_lat']],
#                                 'end_lng': [row['end_lng']],
#                                 'Month_Beginning': [month_beginning]})
#             if i % 4000 == 0:  
#                 df = pd.concat([df, df_chunk], ignore_index=True, axis=1)
#                 df_chunk=pd.DataFrame()
#             else:
#                 df_chunk = pd.concat([df_chunk, new_row], ignore_index=True, axis=1)  
            
#         if df_chunk.shape[0] != 0:
#             df = pd.concat([df, df_chunk], ignore_index=True, axis=1)
#             df_chunk=pd.DataFrame()       
        
   
bus_stop_data = pd.read_csv(bus_route_info_file)
routes_list = bus_stop_data['Routes'].str.split(',')
flat_routes_list = [route for sublist in routes_list for route in sublist]
route_counts = pd.Series(flat_routes_list).value_counts()
route_counts_dict = route_counts.to_dict()

bus_rides_data = pd.read_csv(bus_numbers_file)
monthly_counts = {}

for _, row in bus_rides_data.iterrows():
    month_beginning = row['Month_Beginning']
    route_id = row['route']
    # special case
    if route_id == '14':
        route_id = 'J14'
    month_total = row['MonthTotal']

    if month_beginning in monthly_counts:
        monthly_counts[month_beginning][route_id] = month_total / route_counts_dict.get(route_id, 1)
    else:
        monthly_counts[month_beginning] = {route_id: month_total / route_counts_dict.get(route_id, 1)}

headers= ['Stop_ID','CTA Stop Name','Routes','LONGITUDE','LATITUDE','Month_Beginning','MonthTotal']
df=pd.DataFrame(columns=headers)
df_chunk=pd.DataFrame()
for i, row in bus_stop_data.iterrows():
    routes_list = row['Routes'].split(',')
    for month_beginning, route in monthly_counts.items():
        monthly_stop_count = 0
        for route_id, monthly_rides in route.items():
            if route_id in routes_list:
                monthly_stop_count += monthly_rides
                new_row = pd.DataFrame({'Stop_ID': [row['Stop_ID']],
                                'CTA Stop Name': [row['CTA Stop Name']],
                                'Routes': [row['Routes']],
                                'LONGITUDE': [row['LONGITUDE']],
                                'LATITUDE': [row['LATITUDE']],
                                'Month_Beginning': [month_beginning], 
                                'MonthTotal': [monthly_stop_count]})
        
        # chunking to reduce large concats
        if i % 10 == 0:  
            df = pd.concat([df, df_chunk], ignore_index=True, axis=0)
            df_chunk=pd.DataFrame()
            #print(df.head())
        else:
            df_chunk = pd.concat([df_chunk, new_row], ignore_index=True, axis=0)

if df_chunk.shape[0] != 0:
    df = pd.concat([df, df_chunk], ignore_index=True, axis=1)
    df_chunk=pd.DataFrame()

df.to_csv('monthly_stop_data.csv', index=False)
                    
