# Change: Add Historical Weather Data Tracking

## Why
Currently, the weather app only displays the latest forecast data. Adding historical tracking allows users to compare weather trends over time, see how forecasts change, and analyze patterns across different dates.

## What Changes
- Modify database schema to include timestamp for each data fetch
- Store each API fetch as a new record (not overwrite)
- Add date range selector in the UI
- Display historical trends for selected locations
- **BREAKING**: Database schema changes may require migration

## Impact
- Affected specs: weather-data (new capability)
- Affected code: Database schema, data fetching script, Streamlit app
- Dependencies: None (uses existing SQLite)
