# Change: Add Data Export Functionality

## Why
Users may want to export weather and movie data in different formats (Excel, JSON) for further analysis in other tools like Excel, Google Sheets, or data analysis platforms.

## What Changes
- Add Excel export functionality for weather data
- Add Excel export functionality for movie data
- Add JSON export option for both datasets
- Create export buttons/commands in the application

## Impact
- Affected specs: data-export (new capability)
- Affected code: Streamlit app, movie scraper script
- Dependencies: openpyxl or xlsxwriter (for Excel export)
