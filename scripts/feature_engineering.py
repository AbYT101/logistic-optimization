import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Feature Extraction
def extract_features(df):
    # Parse coordinates and handle NaN values
    df['Trip Origin Lat'] = df['Trip Origin'].apply(lambda x: float(x.split(',')[0]) if pd.notna(x) else np.nan)
    df['Trip Origin Lng'] = df['Trip Origin'].apply(lambda x: float(x.split(',')[1]) if pd.notna(x) else np.nan)
    df['Trip Destination Lat'] = df['Trip Destination'].apply(lambda x: float(x.split(',')[0]) if pd.notna(x) else np.nan)
    df['Trip Destination Lng'] = df['Trip Destination'].apply(lambda x: float(x.split(',')[1]) if pd.notna(x) else np.nan)

    # Convert to datetime and handle NaN values
    df['Trip Start Time'] = pd.to_datetime(df['Trip Start Time'], errors='coerce')
    df['Trip End Time'] = pd.to_datetime(df['Trip End Time'], errors='coerce')
    
    # Calculate trip duration and handle NaN values
    df['trip_duration'] = (df['Trip End Time'] - df['Trip Start Time']).dt.total_seconds() / 60.0
    
    # Calculate trip distance and handle NaN values
    def calculate_distance(row):
        if pd.notna(row['Trip Origin Lat']) and pd.notna(row['Trip Origin Lng']) and pd.notna(row['Trip Destination Lat']) and pd.notna(row['Trip Destination Lng']):
            return geodesic((row['Trip Origin Lat'], row['Trip Origin Lng']), (row['Trip Destination Lat'], row['Trip Destination Lng'])).km
        else:
            return np.nan

    df['trip_distance'] = df.apply(calculate_distance, axis=1)
    
    # Calculate speed and handle NaN values
    df['speed'] = df.apply(lambda row: row['trip_distance'] / (row['trip_duration'] / 60) if pd.notna(row['trip_distance']) and pd.notna(row['trip_duration']) and row['trip_duration'] > 0 else np.nan, axis=1)
    
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