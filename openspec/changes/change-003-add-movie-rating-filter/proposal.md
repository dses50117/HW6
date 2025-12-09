# Change: Add Movie Rating Filter

## Why
The movie scraper collects movies with various ratings. Users may want to filter movies by minimum rating to find only highly-rated content, making the scraped data more useful for decision-making.

## What Changes
- Add rating filter functionality to movie data processing
- Allow filtering movies by minimum rating threshold
- Update CSV output to support filtered results
- Optionally add filtering in a simple viewer script

## Impact
- Affected specs: movie-scraper (new capability)
- Affected code: Movie scraper script, CSV handling
- Dependencies: None
