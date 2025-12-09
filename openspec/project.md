# Project Context

## Purpose
This is a homework assignment (HW6) for the "人工智慧與資訊安全" (AI and Information Security) course. The project contains two main components:
1. **CWA Weather App**: Fetch weather forecast data from the Central Weather Administration (CWA) API, store it in an SQLite database, and display it via a Streamlit web application.
2. **Movie Scraper**: Scrape movie information (name, image URL, rating, type) from a website and save results to a CSV file.

## Tech Stack
- **Language**: Python
- **Web Framework**: Streamlit (for weather app UI)
- **Database**: SQLite (`data.db`)
- **Data Processing**: Pandas
- **HTTP Requests**: requests library
- **Web Scraping**: BeautifulSoup (bs4)
- **Data Format**: JSON (API), CSV (movie data)

## Project Conventions

### Code Style
- Python files use `.py` extension (case-insensitive)
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- OpenSpec change naming: `change-[number]-[verb]-[description]` format

### Architecture Patterns
- Single-file scripts for simple tasks
- Separate concerns: data fetching, storage, and display
- Use SQLite for persistent data storage

### Testing Strategy
- Manual testing via Streamlit app interface
- Screenshot documentation of working features
- Verify database operations work correctly

### Git Workflow
- Feature branches for new development
- Clear, descriptive commit messages

## Domain Context
- **CWA API**: Taiwan's Central Weather Administration provides weather forecast data via REST API (endpoint F-A0010-001)
- **Weather Data Fields**: Location name, minimum temperature, maximum temperature, description
- **Movie Scraping**: Extract structured data from HTML pages with pagination (10 pages)

## Important Constraints
- Must use the provided CWA API key for authentication
- SQLite database must use predefined schema
- Movie scraper must handle 10 pages of content
- Assignment requires screenshot documentation

## External Dependencies
- **CWA API**: `https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-A0010-001`
- **Movie Website**: Target website for scraping movie information
- **Python Libraries**: streamlit, requests, sqlite3, pandas, beautifulsoup4
