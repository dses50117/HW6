## ADDED Requirements

### Requirement: Excel Export
The system SHALL allow exporting data to Excel format (.xlsx).

#### Scenario: Export weather data to Excel
- **WHEN** user clicks the "Export to Excel" button on the weather page
- **THEN** an Excel file containing all weather data is downloaded

#### Scenario: Export movie data to Excel
- **WHEN** user runs export command for movie data
- **THEN** an Excel file containing scraped movie information is created

### Requirement: JSON Export
The system SHALL allow exporting data to JSON format.

#### Scenario: Export weather data to JSON
- **WHEN** user selects JSON export option
- **THEN** a JSON file with structured weather data is downloaded

### Requirement: Download in Streamlit
The system SHALL provide download buttons in the Streamlit interface for data export.

#### Scenario: One-click download
- **WHEN** export button is clicked
- **THEN** the file is immediately downloaded to user's computer
