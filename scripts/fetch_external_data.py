import requests
import pandas as pd

class FetchExternalData:
    @staticmethod
    def fetch_holiday_data(api_key, country, year):
        # Fetch the holiday data from the API
        response = requests.get(f'https://calendarific.com/api/v2/holidays?&api_key={api_key}&country={country}&year={year}')
        holidays = response.json()['response']['holidays']
        
        # Parse the holidays data into a DataFrame
        holiday_data = pd.DataFrame([
            {
                'date': holiday['date']['iso'],
                'name': holiday['name'],
                'type': ', '.join(holiday['type'])
            } 
            for holiday in holidays
        ])
        
        return holiday_data
    
    @staticmethod
    def fetch_weather_data(api_key, start_date, end_date):
        weather_data = []
        date_range = pd.date_range(start=start_date, end=end_date)
        
        for date in date_range:
            timestamp = int(date.timestamp())
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat=6.5244&lon=3.3792&dt={timestamp}&appid={api_key}')
            if response.status_code == 200:
                daily_data = response.json()
                weather_data.append({
                    'date': date.date(),
                    'temperature': daily_data['main']['temp'],
                    'rain': daily_data.get('rain', {}).get('1h', 0),  # Assumes 'rain' field may contain 1 hour rain data
                })
            else:
                print(f"Failed to fetch data for {date.date()}: {response.status_code}")
        
        weather_data = pd.DataFrame(weather_data)
        return weather_data

    @staticmethod
    def fetch_traffic_data(api_key, location, date_range):
        def get_traffic_data(lat, lng, date_time):
            endpoint = "https://traffic.ls.hereapi.com/traffic/6.3/incidents.json"
            params = {
                'apiKey': api_key,
                'bbox': f"{lat-0.05},{lng-0.05};{lat+0.05},{lng+0.05}",
                'criticality': 'critical,major'
            }
            response = requests.get(endpoint, params=params)
            data = response.json()
            
            # Extract relevant traffic information
            traffic_duration = 0
            if 'TRAFFIC_ITEMS' in data and 'TRAFFIC_ITEM' in data['TRAFFIC_ITEMS']:
                for item in data['TRAFFIC_ITEMS']['TRAFFIC_ITEM']:
                    if 'TRAFFIC_ITEM_DESCRIPTION' in item:
                        traffic_duration += item['TRAFFIC_ITEM_DESCRIPTION'][0]['DURATION']
            
            return traffic_duration

        traffic_data = []
        lat, lng = location
        for date in date_range:
            traffic_duration = get_traffic_data(lat, lng, date)
            traffic_data.append({
                'date': date.date(),
                'traffic_duration': traffic_duration
            })
        
        traffic_data = pd.DataFrame(traffic_data)
        return traffic_data
