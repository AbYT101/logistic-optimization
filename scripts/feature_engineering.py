import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Feature Extraction
def extract_features(df):
    # Parse coordinates
    df['Trip Origin Lat'] = df['Trip Origin'].apply(lambda x: float(x.split(',')[0]))
    df['Trip Origin Lng'] = df['Trip Origin'].apply(lambda x: float(x.split(',')[1]))
    df['Trip Destination Lat'] = df['Trip Destination'].apply(lambda x: float(x.split(',')[0]))
    df['Trip Destination Lng'] = df['Trip Destination'].apply(lambda x: float(x.split(',')[1]))

    df['Trip Start Time'] = pd.to_datetime(df['Trip Start Time'])
    df['Trip End Time'] = pd.to_datetime(df['Trip End Time'])
    df['trip_duration'] = (df['Trip End Time'] - df['Trip Start Time']).dt.total_seconds() / 60.0  # Duration in minutes
    df['trip_distance'] = df.apply(lambda row: geodesic((row['Trip Origin Lat'], row['Trip Origin Lng']), (row['Trip Destination Lat'], row['Trip Destination Lng'])).km, axis=1)
    df['speed'] = df['trip_distance'] / (df['trip_duration'] / 60)  # Speed in km/h
    # Weekday or weekend
    df['day_of_week'] = df['Trip Start Time'].dt.dayofweek
    df['is_weekend'] = np.where(df['day_of_week'] >= 5, 1, 0)  # 5 and 6 correspond to Saturday and Sunday
    return df

# Compute the number of riders and orders in circles of 500m
def compute_orders_in_circles(df, lat_col, lng_col, radius=0.5):
    df['coords'] = list(zip(df[lat_col], df[lng_col]))
    circles = []
    for i, row in df.iterrows():
        circle_center = row['coords']
        df['distance'] = df['coords'].apply(lambda x: geodesic(circle_center, x).km)
        circle = df[df['distance'] <= radius]
        circles.append(len(circle))
    df['orders_in_circle'] = circles
    return df