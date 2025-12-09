"""
CWA Weather Streamlit Application - Local Database Version
使用本地預先準備的資料庫，適合快速展示和離線使用
"""

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import folium
from streamlit_folium import folium_static

# Page configuration
st.set_page_config(
    page_title="Taiwan Weather Forecast - Local Version",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* CWA Official Deep Blue Theme */
    .main {
        background-color: #F8F9FA;
    }
    
    /* Header Styling - Deep Blue Gradient */
    h1 {
        color: #003B66;
        font-family: 'Microsoft JhengHei', sans-serif;
        font-weight: 700;
        padding: 20px 0;
        background: linear-gradient(135deg, #003B66 0%, #005697 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2, h3 {
        color: #005697;
        font-family: 'Microsoft JhengHei', sans-serif;
        font-weight: 600;
    }
    
    /* Professional Table Styling */
    .dataframe {
        font-family: 'Microsoft JhengHei', sans-serif;
        border-collapse: collapse;
        width: 100%;
        box-shadow: 0 2px 8px rgba(0,59,102,0.1);
    }
    
    .dataframe thead tr {
        background: linear-gradient(180deg, #003B66 0%, #005697 100%);
        color: white;
        text-align: center;
        font-weight: 700;
        font-size: 14px;
    }
    
    .dataframe thead th {
        padding: 14px 12px;
        border: 1px solid #003B66;
        color: white !important;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #ddd;
        transition: all 0.2s;
    }
    
    .dataframe tbody tr:nth-of-type(even) {
        background-color: #E8F4FF;
    }
    
    .dataframe tbody tr:hover {
        background-color: #D6EBFF;
        transform: scale(1.01);
        box-shadow: 0 2px 4px rgba(0,59,102,0.15);
    }
    
    .dataframe tbody td {
        padding: 12px;
        text-align: center;
        font-size: 13px;
        border-left: 1px solid #E0E0E0;
    }
    
    .dataframe tbody td:first-child {
        font-weight: 600;
        color: #003B66;
        text-align: left;
        background-color: rgba(0,59,102,0.03);
    }
    
    /* Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F8FF 100%);
        padding: 18px;
        border-radius: 10px;
        border-left: 4px solid #005697;
        box-shadow: 0 2px 8px rgba(0,59,102,0.08);
    }
    
    .stMetric label {
        color: #003B66;
        font-weight: 600;
        font-size: 14px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #005697;
        font-size: 28px;
        font-weight: 700;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #003B66 0%, #005697 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #005697 0%, #4A90E2 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0,59,102,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,59,102,0.3);
    }
    
    /* Selectbox Styling */
    .stSelectbox label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Chart Styling */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,59,102,0.1);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #28A745 0%, #20C997 100%);
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 6px;
        font-weight: 600;
    }
    
    /* Info Box */
    .stAlert {
        border-left: 4px solid #005697;
        background-color: #E8F4FF;
        border-radius: 4px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #003B66 0%, #4A90E2 50%, #003B66 100%);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# Database functions
@st.cache_data(ttl=300)
def get_weather_data(location=None, data_type='all'):
    """Fetch weather data from local database"""
    conn = sqlite3.connect('data.db')
    
    if location == 'All Locations':
        if data_type == 'all':
            query = "SELECT location, min_temp, max_temp, description, fetch_time, data_type FROM weather ORDER BY data_type, location"
        else:
            query = f"SELECT location, min_temp, max_temp, description, fetch_time, data_type FROM weather WHERE data_type = '{data_type}' ORDER BY location"
    else:
        if data_type == 'all':
            query = f"SELECT location, min_temp, max_temp, description, fetch_time, data_type FROM weather WHERE location = '{location}' ORDER BY fetch_time DESC"
        else:
            query = f"SELECT location, min_temp, max_temp, description, fetch_time, data_type FROM weather WHERE location = '{location}' AND data_type = '{data_type}' ORDER BY fetch_time DESC"
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def get_latest_weather_data(data_type='all'):
    """Fetch only the latest weather data for each location"""
    conn = sqlite3.connect('data.db')
    
    if data_type == 'all':
        query = """
        SELECT location, min_temp, max_temp, description, fetch_time, data_type 
        FROM weather 
        WHERE fetch_time = (SELECT MAX(fetch_time) FROM weather)
        ORDER BY data_type, location
        """
    else:
        query = f"""
        SELECT location, min_temp, max_temp, description, fetch_time, data_type 
        FROM weather 
        WHERE fetch_time = (SELECT MAX(fetch_time) FROM weather) AND data_type = '{data_type}'
        ORDER BY location
        """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Location coordinates for map
LOCATION_COORDS = {
    # 6 Regions
    '北部地區': [25.0330, 121.5654],
    '中部地區': [24.1477, 120.6736],
    '南部地區': [22.6273, 120.3014],
    '東北部地區': [24.7021, 121.7378],
    '東部地區': [23.9871, 121.6015],
    '東南部地區': [22.7972, 121.0713],
    # 22 Counties
    '臺北市': [25.0375, 121.5625],
    '新北市': [25.0120, 121.4650],
    '基隆市': [25.1276, 121.7392],
    '宜蘭縣': [24.7021, 121.7378],
    '桃園市': [24.9936, 121.3010],
    '新竹市': [24.8138, 120.9675],
    '新竹縣': [24.8387, 121.0177],
    '苗栗縣': [24.5602, 120.8214],
    '臺中市': [24.1477, 120.6736],
    '彰化縣': [24.0518, 120.5161],
    '南投縣': [23.9609, 120.9719],
    '雲林縣': [23.7092, 120.4313],
    '嘉義市': [23.4800, 120.4491],
    '嘉義縣': [23.4518, 120.2554],
    '臺南市': [22.9998, 120.2269],
    '高雄市': [22.6273, 120.3014],
    '屏東縣': [22.5519, 120.5487],
    '臺東縣': [22.7972, 121.0713],
    '花蓮縣': [23.9871, 121.6015],
    '澎湖縣': [23.5711, 119.5793],
    '金門縣': [24.4363, 118.3200],
    '連江縣': [26.1605, 119.9512],
}

def create_weather_map(df):
    """Create interactive Folium map"""
    taiwan_center = [23.5, 121.0]
    m = folium.Map(
        location=taiwan_center,
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    for _, row in df.iterrows():
        location_name = row['location']
        if location_name in LOCATION_COORDS:
            coords = LOCATION_COORDS[location_name]
            
            data_type_zh = '區域' if row.get('data_type') == 'region' else '縣市'
            
            popup_html = f"""
            <div style="font-family: Microsoft JhengHei, sans-serif; width: 200px;">
                <h4 style="margin: 0; color: #003B66;">{location_name}</h4>
                <p style="margin: 3px 0; font-size: 11px; color: #666;">({data_type_zh})</p>
                <hr style="margin: 5px 0;">
                <p style="margin: 5px 0;"><b>🌡️ 最低溫度:</b> {row['min_temp']}°C</p>
                <p style="margin: 5px 0;"><b>🌡️ 最高溫度:</b> {row['max_temp']}°C</p>
                <p style="margin: 5px 0;"><b>☁️ 天氣:</b> {row['description']}</p>
            </div>
            """
            
            if pd.notna(row['max_temp']):
                temp = float(row['max_temp'])
                if temp >= 30:
                    color = 'red'
                elif temp >= 25:
                    color = 'orange'
                elif temp >= 20:
                    color = 'lightblue'
                else:
                    color = 'blue'
            else:
                color = 'gray'
            
            folium.CircleMarker(
                location=coords,
                radius=8,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{location_name}: {row['max_temp']}°C",
                color=color,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
    
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 150px; height: 140px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px; border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
    <p style="margin: 0 0 10px 0; font-weight: bold; text-align: center;">Temperature</p>
    <p style="margin: 5px 0;"><span style="color: red;">●</span> ≥ 30°C (High)</p>
    <p style="margin: 5px 0;"><span style="color: orange;">●</span> 25-30°C</p>
    <p style="margin: 5px 0;"><span style="color: lightblue;">●</span> 20-25°C</p>
    <p style="margin: 5px 0;"><span style="color: blue;">●</span> < 20°C (Low)</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

def main():
    # Header with version indicator
    st.title("🌤️ Taiwan Weather Forecast - Local Version")
    st.markdown("### 📊 Using Pre-loaded Database | 使用本地資料庫")
    st.divider()
    
    # Check if database exists and has data
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather")
        count = cursor.fetchone()[0]
        cursor.execute("SELECT MAX(fetch_time) FROM weather")
        last_update = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            st.error("❌ Database is empty!")
            st.info("""
            **Please initialize the database first:**
            ```bash
            python fetch_weather.py
            ```
            This will fetch weather data for all 28 locations from CWA API.
            """)
            st.stop()
        else:
            st.success(f"✅ Database loaded: {count} records | Last update: {last_update}")
            
    except sqlite3.OperationalError:
        st.error("❌ Database not found!")
        st.info("""
        **Please create the database first:**
        ```bash
        python fetch_weather.py
        ```
        This will create `data.db` and fetch weather data for all 28 locations.
        """)
        st.stop()
    
    # Fetch data
    try:
        # Sidebar options
        st.sidebar.header("⚙️ Options")
        
        # Data type filter
        data_type_options = {
            'All Types': 'all',
            'Regions (6)': 'region',
            'Counties (22)': 'county'
        }
        selected_type_label = st.sidebar.selectbox(
            "📍 Data Type",
            options=list(data_type_options.keys())
        )
        selected_type = data_type_options[selected_type_label]
        
        # Get latest data for location dropdown
        latest_df = get_latest_weather_data(selected_type)
        
        if latest_df.empty:
            st.warning("No weather data available.")
            st.stop()
        
        locations = ['All Locations'] + sorted(latest_df['location'].unique().tolist())
        selected_location = st.sidebar.selectbox("📍 Select Location", options=locations)
        
        # Historical data toggle
        show_historical = st.sidebar.checkbox("📈 Show Historical Data", value=False)
        
        # Chart type selection
        chart_type = st.sidebar.radio("📊 Chart Type", options=["Bar Chart", "Line Chart"])
        
        # Fetch data based on selection
        if show_historical:
            df = get_weather_data(selected_location, selected_type)
        else:
            if selected_location == 'All Locations':
                df = latest_df
            else:
                df = latest_df[latest_df['location'] == selected_location]
        
        if df.empty:
            st.warning(f"No data available for {selected_location}")
            st.stop()
        
        # Statistics
        st.markdown("### 📊 Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label=f"Locations ({selected_type_label})",
                value=f"{len(df['location'].unique())} total"
            )
        
        with col2:
            avg_min = df['min_temp'].mean()
            st.metric(
                label="Average Min Temperature",
                value=f"{avg_min:.1f}°C" if pd.notna(avg_min) else "N/A"
            )
        
        with col3:
            avg_max = df['max_temp'].mean()
            st.metric(
                label="Average Max Temperature",
                value=f"{avg_max:.1f}°C" if pd.notna(avg_max) else "N/A"
            )
        
        st.divider()
        
        # Interactive Map
        st.markdown("### 🗺️ Interactive Weather Map")
        map_df = latest_df if selected_location == 'All Locations' else df.head(1)
        weather_map = create_weather_map(map_df)
        folium_static(weather_map, width=1200, height=500)
        
        st.divider()
        
        # Chart Visualization
        st.markdown("### 📈 Temperature Visualization")
        
        if chart_type == "Bar Chart":
            import plotly.graph_objects as go
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Min Temperature',
                x=df['location'],
                y=df['min_temp'],
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Max Temperature',
                x=df['location'],
                y=df['max_temp'],
                marker_color='coral'
            ))
            
            fig.update_layout(
                title='Temperature Comparison',
                xaxis_title='Location',
                yaxis_title='Temperature (°C)',
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        else:  # Line Chart
            import plotly.express as px
            
            df_melted = df.melt(
                id_vars=['location', 'fetch_time'], 
                value_vars=['min_temp', 'max_temp'],
                var_name='Type',
                value_name='Temperature'
            )
            
            fig = px.line(
                df_melted,
                x='location' if not show_historical else 'fetch_time',
                y='Temperature',
                color='Type',
                title='Temperature Trend',
                markers=True
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Data Table
        st.markdown("### 📋 Weather Data Table")
        
        display_df = df[['location', 'min_temp', 'max_temp', 'description', 'fetch_time']].copy()
        display_df.columns = ['Location', 'Min Temp (°C)', 'Max Temp (°C)', 'Description', 'Fetch Time']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Data Export
        st.markdown("### 💾 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Download as Excel (CSV)",
                data=csv,
                file_name=f'weather_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
        
        with col2:
            json_str = df.to_json(orient='records', force_ascii=False, indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f'weather_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
                mime='application/json'
            )
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
