"""
CWA Weather Streamlit App
Displays weather forecast data with location dropdown selector.
Enhanced with 28 locations (6 regions + 22 counties).
"""

import streamlit as st
import sqlite3
import pandas as pd
import io
import json
from datetime import datetime
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="CWA Weather Forecast",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS for authentic CWA official website design
st.markdown("""
<style>
    /* Official CWA Color Scheme */
    :root {
        --cwa-deep-blue: #003B66;
        --cwa-primary-blue: #005697;
        --cwa-light-blue: #4A90E2;
        --cwa-bg-gray: #F5F5F5;
        --cwa-border: #DDDDDD;
        --cwa-text-dark: #333333;
        --cwa-table-header: #003B66;
        --cwa-table-row-alt: #E8F4FF;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* CWA-style header with deep blue background */
    h1 {
        background: linear-gradient(135deg, var(--cwa-deep-blue) 0%, var(--cwa-primary-blue) 100%);
        color: white !important;
        padding: 1.5rem 2rem !important;
        margin: -2rem -2rem 2rem -2rem !important;
        border-radius: 0 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        border-bottom: 4px solid var(--cwa-light-blue);
    }
    
    /* Section headers */
    h2 {
        color: var(--cwa-deep-blue) !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        margin-top: 2rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 3px solid var(--cwa-primary-blue) !important;
    }
    
    h3 {
        color: var(--cwa-primary-blue) !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
    }
    
    /* Professional CWA table styling */
    .stDataFrame {
        border: 2px solid var(--cwa-border) !important;
        border-radius: 0 !important;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        font-family: "Microsoft JhengHei", "微軟正黑體", Arial, sans-serif !important;
    }
    
    /* Table header - deep blue like CWA */
    .stDataFrame thead tr {
        background: linear-gradient(180deg, var(--cwa-table-header) 0%, var(--cwa-primary-blue) 100%) !important;
    }
    
    .stDataFrame th {
        color: white !important;
        font-weight: 700 !important;
        padding: 14px 12px !important;
        text-align: center !important;
        font-size: 0.95rem !important;
        border-right: 1px solid rgba(255,255,255,0.2) !important;
        letter-spacing: 0.5px;
    }
    
    /* Table body rows */
    .stDataFrame tbody tr {
        border-bottom: 1px solid var(--cwa-border) !important;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background-color: var(--cwa-table-row-alt) !important;
    }
    
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: white !important;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #D6EBFF !important;
        transition: background-color 0.2s ease;
    }
    
    .stDataFrame td {
        padding: 12px !important;
        color: var(--cwa-text-dark) !important;
        font-size: 0.9rem !important;
        border-right: 1px solid #E8E8E8 !important;
        text-align: center !important;
    }
    
    /* First column (location) - left aligned */
    .stDataFrame td:first-child {
        font-weight: 600 !important;
        text-align: left !important;
        color: var(--cwa-deep-blue) !important;
    }
    
    /* Metric cards - CWA style */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        color: var(--cwa-primary-blue) !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--cwa-text-dark) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stMetric {
        background-color: white !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 2px solid var(--cwa-border) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
    }
    
    /* Sidebar - clean white design */
    [data-testid="stSidebar"] {
        background-color: #FAFAFA;
        border-right: 3px solid var(--cwa-primary-blue);
    }
    
    [data-testid="stSidebar"] h2 {
        color: var(--cwa-deep-blue) !important;
        font-size: 1.1rem !important;
        border-bottom: 2px solid var(--cwa-primary-blue) !important;
    }
    
    /* Download buttons - CWA blue gradient */
    .stDownloadButton button {
        background: linear-gradient(135deg, var(--cwa-primary-blue) 0%, var(--cwa-light-blue) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,91,151,0.3) !important;
        text-transform: none !important;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, var(--cwa-deep-blue) 0%, var(--cwa-primary-blue) 100%) !important;
        box-shadow: 0 4px 8px rgba(0,59,102,0.4) !important;
        transform: translateY(-1px);
    }
    
    /* Radio buttons - CWA style */
    .stRadio [role="radiogroup"] {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
    }
    
    .stRadio [role="radio"] {
        background-color: white;
        border: 2px solid var(--cwa-primary-blue);
        padding: 0.5rem 1.2rem;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .stRadio [role="radio"]:hover {
        background-color: var(--cwa-table-row-alt);
        border-color: var(--cwa-deep-blue);
    }
    
    /* Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid var(--cwa-border);
    }
    
    /* Charts */
    .stChart {
        border: 2px solid var(--cwa-border);
        border-radius: 4px;
        padding: 1rem;
        background-color: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    
    /* Map container */
    .folium-map {
        border: 2px solid var(--cwa-border) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        padding: 0.5rem;
        background-color: white;
        border-radius: 4px;
    }
    
    /* Select box */
    .stSelectbox {
        background-color: white;
    }
    
</style>
""", unsafe_allow_html=True)

def get_weather_data():
    """Fetch all weather data from database."""
    conn = sqlite3.connect('data.db')
    query = "SELECT location, min_temp, max_temp, description, fetch_time, data_type FROM weather ORDER BY fetch_time DESC, data_type, location"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_latest_weather_data():
    """Fetch only the most recent weather data."""
    conn = sqlite3.connect('data.db')
    # Get the most recent fetch_time
    query = """
    SELECT location, min_temp, max_temp, description, fetch_time, data_type
    FROM weather 
    WHERE fetch_time = (SELECT MAX(fetch_time) FROM weather)
    ORDER BY data_type, location
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Taiwan region and county coordinates for map markers (28 locations total)
LOCATION_COORDS = {
    # 6 大區域 (Regions)  
    '北部地區': [25.0330, 121.5654],  # Taipei area
    '中部地區': [24.1477, 120.6736],  # Taichung area
    '南部地區': [22.9908, 120.2133],  # Kaohsiung/Tainan area
    '東北部地區': [24.7500, 121.7500], # Yilan area
    '東部地區': [23.9769, 121.6069],   # Hualien area
    '東南部地區': [22.7553, 121.1440], # Taitung area
    
    # 22 縣市 (Counties)
    '臺北市': [25.0375, 121.5625],    # Taipei City
    '新北市': [25.0120, 121.4650],    # New Taipei City
    '基隆市': [25.1276, 121.7392],    # Keelung City
    '宜蘭縣': [24.7021, 121.7378],    # Yilan County
    '桃園市': [24.9936, 121.3010],    # Taoyuan City
    '新竹市': [24.8138, 120.9675],    # Hsinchu City
    '新竹縣': [24.8387, 121.0177],    # Hsinchu County
    '苗栗縣': [24.5602, 120.8214],    # Miaoli County
    '臺中市': [24.1477, 120.6736],    # Taichung City
    '彰化縣': [24.0518, 120.5161],    # Changhua County
    '南投縣': [23.9609, 120.9719],    # Nantou County
    '雲林縣': [23.7092, 120.4313],    # Yunlin County
    '嘉義市': [23.4800, 120.4491],    # Chiayi City
    '嘉義縣': [23.4518, 120.2554],    # Chiayi County
    '臺南市': [22.9998, 120.2269],    # Tainan City
    '高雄市': [22.6273, 120.3014],    # Kaohsiung City
    '屏東縣': [22.5519, 120.5487],    # Pingtung County
    '臺東縣': [22.7972, 121.0713],    # Taitung County
    '花蓮縣': [23.9871, 121.6015],    # Hualien County
    '澎湖縣': [23.5711, 119.5793],    # Penghu County
    '金門縣': [24.4489, 118.3765],    # Kinmen County
    '連江縣': [26.1605, 119.9500]     # Lienchiang County (Matsu)
}

def create_weather_map(df):
    """Create interactive weather map with Leaflet."""
    # Center map on Taiwan
    taiwan_center = [23.5, 121.0]
    m = folium.Map(
        location=taiwan_center,
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add markers for each location with weather data
    for _, row in df.iterrows():
        location_name = row['location']
        
        if location_name in LOCATION_COORDS:
            coords = LOCATION_COORDS[location_name]
            
            # Determine data type for display
            data_type_label = "區域" if row.get('data_type') == 'region' else "縣市"
            
            # Create popup content with weather info
            popup_html = f"""
            <div style="font-family: sans-serif; width: 200px;">
                <h4 style="margin: 0; color: #003B66;">{location_name}</h4>
                <p style="margin: 2px 0; font-size: 0.85em; color: #666;">({data_type_label})</p>
                <hr style="margin: 5px 0;">
                <p style="margin: 5px 0;"><b>🌡️ 最低溫度:</b> {row['min_temp']}°C</p>
                <p style="margin: 5px 0;"><b>🌡️ 最高溫度:</b> {row['max_temp']}°C</p>
                <p style="margin: 5px 0;"><b>☁️ 天氣:</b> {row['description']}</p>
            </div>
            """
            
            # Color code based on max temperature
            if pd.notna(row['max_temp']):
                max_temp = float(row['max_temp'])
                if max_temp >= 30:
                    color = 'red'
                elif max_temp >= 25:
                    color = 'orange'
                elif max_temp >= 20:
                    color = 'lightblue'
                else:
                    color = 'blue'
            else:
                color = 'gray'
            
            # Add marker
            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{location_name}: {row['max_temp']}°C",
                icon=folium.Icon(color=color, icon='cloud', prefix='fa')
            ).add_to(m)
    
    return m

def main():
    # Header
    st.title("🌤️ Taiwan Weather Forecast (28 Locations)")
    st.markdown("### Central Weather Administration (CWA) Data")
    st.divider()
    
    # Check if database exists and has data
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            st.warning("⚠️ Database is empty. Please initialize the database first.")
            st.info("""
            **To fetch weather data, run:**
            ```bash
            python fetch_weather.py
            ```
            This will fetch weather data for all 28 locations from CWA API.
            """)
            st.stop()
    except sqlite3.OperationalError:
        # Database table doesn't exist
        st.error("❌ Database not found or not initialized.")
        st.info("""
        **First Time Setup Required:**
        
        Please run the following command to initialize the database and fetch weather data:
        ```bash
        python fetch_weather.py
        ```
        
        This will:
        - Create the SQLite database (`data.db`)
        - Fetch weather data from CWA API for all 28 locations
        - Store data in the database
        
        After running the command, refresh this page.
        """)
        st.stop()
    
    # Fetch data
    try:
        # Sidebar options
        st.sidebar.header("🔍 Filter Options")
        
        # Historical data toggle
        show_historical = st.sidebar.checkbox("Show Historical Data", value=False)
        
        if show_historical:
            df = get_weather_data()  # All data
        else:
            df = get_latest_weather_data()  # Latest only
        
        if df.empty:
            st.warning(" No weather data available. Please run `python fetch_weather.py` first.")
            return
        
        # Data type filter (Region/County/All)
        if 'data_type' in df.columns:
            data_type_options = ["All Types", "Regions (6)", "Counties (22)"]
            selected_type = st.sidebar.selectbox("Select Data Type:", data_type_options, index=0)
            
            if selected_type == "Regions (6)":
                df = df[df['data_type'] == 'region']
            elif selected_type == "Counties (22)":
                df = df[df['data_type'] == 'county']
        
        # Location dropdown selector
        locations = ["All Locations"] + sorted(df['location'].unique().tolist())
        selected_location = st.sidebar.selectbox(
            "Select Location:",
            locations,
            index=0
        )
        
        # Filter data based on selection
        if selected_location == "All Locations":
            filtered_df = df
            st.subheader(f"📊 All Locations ({len(df['location'].unique())} total)")
        else:
            filtered_df = df[df['location'] == selected_location]
            st.subheader(f"📍 {selected_location}")
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="📍 Locations",
                value=len(filtered_df['location'].unique())
            )
        
        with col2:
            if not filtered_df.empty and filtered_df['min_temp'].notna().any():
                avg_min = filtered_df['min_temp'].mean()
                st.metric(
                    label="🌡️ Avg Min Temp",
                    value=f"{avg_min:.1f}°C"
                )
        
        with col3:
            if not filtered_df.empty and filtered_df['max_temp'].notna().any():
                avg_max = filtered_df['max_temp'].mean()
                st.metric(
                    label="🌡️ Avg Max Temp",
                    value=f"{avg_max:.1f}°C"
                )
        
        st.divider()
        
        # Interactive Weather Map Section
        st.subheader("🗺️ Interactive Weather Map")
        st.markdown("點擊地圖上的標記查看詳細天氣資訊 (Click markers for weather details)")
        
        # Create and display map
        weather_map = create_weather_map(filtered_df.drop_duplicates(subset=['location']))
        st_folium(weather_map, width=1200, height=500)
        
        st.markdown("""
        **地圖說明 (Map Legend):**
        - 🔴 紅色 (Red): 高溫 ≥ 30°C
        - 🟠 橙色 (Orange): 溫度 25-30°C  
        - 🔵 淺藍色 (Light Blue): 溫度 20-25°C
        - 🔵 藍色 (Blue): 低溫 < 20°C
        """)
        
        st.divider()
        
        # Chart Visualization Section
        st.subheader("📊 Temperature Visualization")
        
        # Chart type selector
        chart_type = st.radio(
            "Select Chart Type:",
            ["Bar Chart", "Line Chart"],
            horizontal=True
        )
        
        if not filtered_df.empty:
            # Group by location and get latest data for chart
            chart_df = filtered_df.drop_duplicates(subset=['location'], keep='first')
            if chart_type == "Bar Chart":
                # Bar chart for min/max temperatures
                chart_data = chart_df[['location', 'min_temp', 'max_temp']].set_index('location')
                st.bar_chart(chart_data)
            else:
                # Line chart for min/max temperatures
                chart_data = chart_df[['location', 'min_temp', 'max_temp']].set_index('location')
                st.line_chart(chart_data)
        
        st.divider()
        
        # Data Export Section
        st.subheader("💾 Export Data")
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # Excel export
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Weather Data')
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download Excel",
                data=buffer,
                file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col_export2:
            # JSON export
            json_data = filtered_df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        st.divider()
        
        # Display data table
        display_columns = ['location', 'min_temp', 'max_temp', 'description']
        if 'data_type' in filtered_df.columns:
            display_columns.append('data_type')
        if 'fetch_time' in filtered_df.columns:
            display_columns.append('fetch_time')
        
        st.dataframe(
            filtered_df[display_columns],
            column_config={
                "location": st.column_config.TextColumn("Location", width="medium"),
                "min_temp": st.column_config.NumberColumn("Min Temp (°C)", width="small", format="%.1f"),
                "max_temp": st.column_config.NumberColumn("Max Temp (°C)", width="small", format="%.1f"),
                "description": st.column_config.TextColumn("Weather Description", width="large"),
                "data_type": st.column_config.TextColumn("Type", width="small"),
                "fetch_time": st.column_config.DatetimeColumn("Fetch Time", width="medium")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Footer
        st.divider()
        st.caption(f"Data source: Central Weather Administration (CWA) Taiwan | Total Locations: {len(df['location'].unique())}")
        
    except sqlite3.OperationalError:
        st.error("❌ Database not found. Please run `python fetch_weather.py` to create and populate the database.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
