import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Point

# Assuming station_data is a pandas DataFrame with the required columns
station_data = pd.DataFrame(...)  # Load station data

# Converting the DataFrame to a GeoDataFrame
geometry = [Point(xy) for xy in zip(station_data['longitude'], station_data['latitude'])]
station_data = station_data.drop(['longitude', 'latitude'], axis=1)
gdf = gpd.GeoDataFrame(station_data, crs="EPSG:4326", geometry=geometry)

# Spatial visualization: plot the stations on a map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
ax = world.plot(color='white', edgecolor='black')
gdf.plot(ax=ax, marker='o', column='user_count', cmap='viridis', legend=True)
plt.show()

# Temporal visualization: plot the number of users over time for a specific station
station_id = 'station_0'
station_data = gdf[gdf['station_id'] == station_id]
station_data = station_data.set_index('timestamp')
station_data['user_count'].plot(kind='line')
plt.xlabel('Timestamp')
plt.ylabel('User count')
plt.title(f'User count over time for {station_id}')
plt.show()

# Heatmap visualization: show the relationship between different variables
heatmap_data = gdf[['timestamp', 'station_id', 'user_count']]
heatmap_data = heatmap_data.pivot_table(index='timestamp', columns='station_id', values='user_count')
sns.heatmap(heatmap_data, cmap='viridis')
plt.xlabel('Station ID')
plt.ylabel('Timestamp')
plt.title('User count per station and timestamp')
plt.show()

def prepare_data_for_analysis(user_behavior_data):
    data = []

    for user_id, user_data in user_behavior_data.items():
        for song_id, song_data in user_data.items():
            data.append({
                "user_id": user_id,
                "song_id": song_id,
                "latitude": song_data["location"][0],
                "longitude": song_data["location"][1],
                "timestamp": song_data["timestamp"],
                "listening_count": len(song_data["listening_time"]),
                "genre": song_data["genre"]
            })

    return pd.DataFrame(data)

# Assuming user_behavior_data is already loaded from the saved file
user_behavior_df = prepare_data_for_analysis(user_behavior_data)


# Convert the DataFrame to a GeoDataFrame
geometry = [Point(xy) for xy in zip(user_behavior_df['longitude'], user_behavior_df['latitude'])]
user_behavior_df = user_behavior_df.drop(['longitude', 'latitude'], axis=1)
gdf = gpd.GeoDataFrame(user_behavior_df, crs="EPSG:4326", geometry=geometry)

# Spatial visualization: plot the listening locations on a map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
ax = world.plot(color='white', edgecolor='black')
gdf.plot(ax=ax, marker='o', column='listening_count', cmap='viridis', legend=True)
plt.show()

# Temporal visualization: plot the listening count by time of day
user_behavior_df['hour'] = user_behavior_df['timestamp'].dt.hour
hourly_listening_count = user_behavior_df.groupby('hour')['listening_count'].sum().reset_index()
sns.barplot(x='hour', y='listening_count', data=hourly_listening_count)
plt.xlabel('Hour of the day')
plt.ylabel('Listening count')
plt.title('Listening count by time of day')
plt.show()

# Spatial-temporal visualization: plot the listening count by location and time of day
gdf['hour'] = gdf['timestamp'].dt.hour
gdf_by_hour = gdf.groupby(['hour', 'geometry'])['listening_count'].sum().reset_index()
gdf_by_hour = gpd.GeoDataFrame(gdf_by_hour, crs="EPSG:4326", geometry='geometry')

for hour in range(24):
    ax = world.plot(color='white', edgecolor='black')
    gdf_by_hour[gdf_by_hour['hour'] == hour].plot(ax=ax, marker='o', column='listening_count', cmap='viridis', legend=True)
    plt.title(f'Listening count by location at hour {hour}')
    plt.show()

#plots
#The listening locations on a map, with markers colored based on the listening count.
#The listening count by the time of day in a bar chart.
#The listening count by location at each hour of the day on separate maps.
