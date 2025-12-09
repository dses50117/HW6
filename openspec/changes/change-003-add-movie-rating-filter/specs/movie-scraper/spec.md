## ADDED Requirements

### Requirement: Movie Rating Filter
The system SHALL allow filtering of scraped movies based on minimum rating threshold.

#### Scenario: Filter by minimum rating
- **WHEN** user specifies a minimum rating (e.g., 7.0)
- **THEN** only movies with ratings >= the threshold are included in output

#### Scenario: Handle missing ratings
- **WHEN** a movie has no rating or invalid rating data
- **THEN** the movie is excluded from filtered results (or marked as "N/A")

### Requirement: Rating-Based Sorting
The system SHALL support sorting movies by rating in descending order.

#### Scenario: Sort by highest rating
- **WHEN** user requests sorted output
- **THEN** movies are displayed with highest-rated movies first
