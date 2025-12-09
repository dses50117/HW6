"""
CWA Weather Data Fetcher - Enhanced with 22 Counties
Fetches both regional (6) and county (22) weather forecast data from CWA API.
Supports TWO different county API formats.
"""

import requests
import sqlite3
import json
from datetime import datetime
import time

# CWA API Configuration
REGIONAL_API_URL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001"
REGIONAL_API_KEY = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"

COUNTY_API_KEY = "CWA-67B3E062-3904-46EE-A0C9-C68C296349FD"
COUNTY_API_BASE = "https://opendata.cwa.gov.tw/api/v1/rest/datastore"

# 22 縣市端點編號對照
COUNTY_ENDPOINTS = {
    '001': '臺北市', '003': '新北市', '007': '基隆市',
    '009': '宜蘭縣', '011': '桃園市', '013': '新竹市',
    '015': '新竹縣', '017': '苗栗縣', '019': '臺中市',
    '021': '彰化縣', '023': '南投縣', '025': '雲林縣',
    '027': '嘉義市', '029': '嘉義縣', '031': '臺南市',
    '033': '高雄市', '035': '屏東縣', '037': '臺東縣',
    '039': '花蓮縣', '041': '澎湖縣', '043': '金門縣',
    '045': '連江縣'
}

def create_database():
    """Create SQLite database and weather table if not exists."""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # 檢查 data_type 欄位是否存在
    cursor.execute("PRAGMA table_info(weather)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'data_type' not in columns:
        try:
            cursor.execute('ALTER TABLE weather ADD COLUMN data_type TEXT DEFAULT "region"')
            print("✓ Added data_type column to database")
        except:
            pass
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            min_temp REAL,
            max_temp REAL,
            description TEXT,
            fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_type TEXT DEFAULT 'region'
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database ready")

def fetch_regional_weather():
    """Fetch 6 regional weather data from F-A0010-001."""
    try:
        url = f"{REGIONAL_API_URL}?Authorization={REGIONAL_API_KEY}&format=JSON"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"✗ Error fetching regional data: {e}")
        return None

def fetch_county_weather(code):
    """Fetch county weather data from F-D0047-XXX."""
    try:
        endpoint = f"F-D0047-{code}"
        url = f"{COUNTY_API_BASE}/{endpoint}?Authorization={COUNTY_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return None

def parse_regional_data(data):
    """Parse regional weather data (6 regions)."""
    locations_data = []
    
    try:
        locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
        
        for location in locations:
            location_name = location.get('locationName', 'Unknown')
            weather_elements = location.get('weatherElements', {})
            
            min_temp = None
            max_temp = None
            description = 'N/A'
            
            # Get MaxT
            max_t_data = weather_elements.get('MaxT', {})
            max_t_daily = max_t_data.get('daily', [])
            if max_t_daily:
                temp_str = max_t_daily[0].get('temperature', 'N/A')
                max_temp = float(temp_str) if temp_str != 'N/A' else None
            
            # Get MinT
            min_t_data = weather_elements.get('MinT', {})
            min_t_daily = min_t_data.get('daily', [])
            if min_t_daily:
                temp_str = min_t_daily[0].get('temperature', 'N/A')
                min_temp = float(temp_str) if temp_str != 'N/A' else None
            
            # Get Weather description
            wx_data = weather_elements.get('Wx', {})
            wx_daily = wx_data.get('daily', [])
            if wx_daily:
                description = wx_daily[0].get('weather', 'N/A')
            
            locations_data.append({
                'location': location_name,
                'min_temp': min_temp,
                'max_temp': max_temp,
                'description': description,
                'data_type': 'region'
            })
            
            print(f"  → {location_name}: {min_temp}°C ~ {max_temp}°C, {description}")
    
    except Exception as e:
        print(f"✗ Error parsing regional data: {e}")
    
    return locations_data

def parse_county_data(data, county_name):
    """Parse county weather data - supports TWO different API formats."""
    try:
        locations = data['records']['Locations'][0]['Location']
        
        # 收集所有鄉鎮的溫度資料
        all_temps = []  # 用於格式2（只有溫度）
        temps_min = []  # 用於格式1（有最高/最低溫度）
        temps_max = []
        descriptions = set()
        
        api_format = None  # 偵測API格式
        
        for loc in locations:
            weather_elements = loc.get('WeatherElement', [])
            
            for element in weather_elements:
                element_name = element.get('ElementName', '')
                time_data = element.get('Time', [])
                
                if not time_data:
                    continue
                
                # 偵測API格式
                if element_name == '最低溫度':
                    api_format = 'format1'  # 12小時預報，有Min/Max
                elif element_name == '溫度' and api_format is None:
                    api_format = 'format2'  # 逐小時預報，只有溫度
                
                # 格式1：有最高/最低溫度欄位
                if element_name == '最低溫度':
                    for time_entry in time_data:
                        values = time_entry.get('ElementValue', [])
                        if values:
                            min_val = values[0].get('MinTemperature')
                            if min_val:
                                try:
                                    temps_min.append(float(min_val))
                                except (ValueError, TypeError):
                                    pass
                
                elif element_name == '最高溫度':
                    for time_entry in time_data:
                        values = time_entry.get('ElementValue', [])
                        if values:
                            max_val = values[0].get('MaxTemperature')
                            if max_val:
                                try:
                                    temps_max.append(float(max_val))
                                except (ValueError, TypeError):
                                    pass
                
                # 格式2：只有溫度欄位（逐小時）
                elif element_name == '溫度':
                    for time_entry in time_data:
                        values = time_entry.get('ElementValue', [])
                        if values:
                            temp_val = values[0].get('Temperature')
                            if temp_val:
                                try:
                                    all_temps.append(float(temp_val))
                                except (ValueError, TypeError):
                                    pass
                
                # 天氣現象
                elif element_name in ['天氣現象', '天氣預報綜合描述']:
                    # 只取幾個代表性時間點的天氣
                    sample_times = time_data[:5] if len(time_data) > 5 else time_data
                    for time_entry in sample_times:
                        values = time_entry.get('ElementValue', [])
                        if values:
                            weather_desc = values[0].get('Weather') or values[0].get('WeatherDescription', '')
                            if weather_desc and weather_desc not in descriptions:
                                descriptions.add(weather_desc)
        
        # 根據API格式計算溫度
        if api_format == 'format1' and temps_min and temps_max:
            # 格式1：直接使用最高/最低溫度
            min_temp = sum(temps_min) / len(temps_min)
            max_temp = sum(temps_max) / len(temps_max)
        elif api_format == 'format2' and all_temps:
            # 格式2：從所有溫度資料中計算最高/最低
            min_temp = min(all_temps)
            max_temp = max(all_temps)
        else:
            # 沒有資料
            min_temp = None
            max_temp = None
        
        description = ' / '.join(list(descriptions)[:3]) if descriptions else 'N/A'
        
        return {
            'location': county_name,
            'min_temp': round(min_temp, 1) if min_temp else None,
            'max_temp': round(max_temp, 1) if max_temp else None,
            'description': description,
            'data_type': 'county'
        }
    
    except Exception as e:
        print(f"  ✗ {county_name}: Error - {e}")
        return None

def store_weather_data(locations_data):
    """Store weather data in SQLite database."""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    stored_count = 0
    for loc_data in locations_data:
        try:
            cursor.execute('''
                INSERT INTO weather (location, min_temp, max_temp, description, data_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                loc_data['location'],
                loc_data['min_temp'],
                loc_data['max_temp'],
                loc_data['description'],
                loc_data['data_type']
            ))
            stored_count += 1
        except Exception as e:
            print(f"✗ Error storing {loc_data['location']}: {e}")
    
    conn.commit()
    conn.close()
    
    return stored_count

def main():
    print("=" * 60)
    print("CWA Weather Data Fetcher (6 Regions + 22 Counties)")
    print("=" * 60)
    
    # Create database
    create_database()
    
    all_locations = []
    
    # Fetch 6 regional data
    print("\n1️⃣  Fetching 6 Regional Weather Data...")
    regional_data = fetch_regional_weather()
    if regional_data:
        print("✓ Regional API Response received")
        print("\nParsing regional weather data...")
        regional_locations = parse_regional_data(regional_data)
        all_locations.extend(regional_locations)
        print(f"✓ Parsed {len(regional_locations)} regions")
    
    # Fetch 22 county data
    print("\n2️⃣  Fetching 22 County Weather Data...")
    county_count = 0
    for code, name in COUNTY_ENDPOINTS.items():
        print(f"  Fetching {name}...", end=' ')
        county_data = fetch_county_weather(code)
        
        if county_data:
            county_loc = parse_county_data(county_data, name)
            if county_loc:
                all_locations.append(county_loc)
                county_count += 1
                if county_loc['min_temp'] and county_loc['max_temp']:
                    print(f"✓ {county_loc['min_temp']}°C ~ {county_loc['max_temp']}°C")
                else:
                    print("✓")
        else:
            print("✗ Failed")
        
        # 避免請求過快
        time.sleep(0.5)
    
    print(f"\n✓ Successfully fetched {county_count} counties")
    
    # Store all data
    print("\n3️⃣  Storing data to database...")
    stored = store_weather_data(all_locations)
    print(f"✓ Stored {stored} location records")
    
    print("\n" + "=" * 60)
    print(f"✓ Total: {len(all_locations)} locations (6 regions + {county_count} counties)")
    print("=" * 60)

if __name__ == "__main__":
    main()
