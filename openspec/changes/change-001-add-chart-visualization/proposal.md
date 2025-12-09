# Change: Add Chart Visualization for Weather Data

## Why
The current weather display shows data in a table format only. Adding charts and graphs will help users quickly visualize temperature trends across different locations, making the data more intuitive and engaging.

## What Changes
- Add temperature bar charts comparing min/max temperatures across locations
- Add interactive visualization using Streamlit's built-in charting capabilities
- Enhance the weather display page with visual data representation

## Impact
- Affected specs: weather-display (new capability)
- Affected code: Streamlit weather app (`app.py` or equivalent)
- Dependencies: matplotlib or plotly (optional, can use Streamlit's native charts)
