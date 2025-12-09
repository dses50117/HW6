"""
Movie Data Scraper
Scrapes movie information from IMDb and supports filtering by minimum rating.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import time

def scrape_movies(num_pages=10, min_rating=0.0, sort_by_rating=False):
    """
    Scrape movie data from IMDb top movies.
    
    Args:
        num_pages: Number of pages to scrape
        min_rating: Minimum rating threshold (0.0-10.0)
        sort_by_rating: Sort movies by rating (highest first)
    """
    movies = []
    base_url = "https://www.imdb.com/search/title/"
    
    print(f"=" * 60)
    print(f"Movie Scraper - Scraping {num_pages} page(s)")
    if min_rating >0:
        print(f"Min Rating Filter: {min_rating}+")
    print(f"=" * 60)
    
    for page in range(1, num_pages + 1):
        params = {
            'title_type': 'feature',
            'sort': 'user_rating,desc',
            'start': (page - 1) * 50 + 1
        }
        
        try:
            print(f"\nScraping page {page}...")
            response = requests.get(base_url, params=params, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            movie_cards = soup.find_all('div', class_='lister-item mode-advanced')
            
            for card in movie_cards:
                try:
                    # Extract movie name
                    title_element = card.find('h3', class_='lister-item-header').find('a')
                    name = title_element.text.strip() if title_element else 'N/A'
                    
                    # Extract image URL
                    img_element = card.find('img', class_='loadlate')
                    image_url = img_element['loadlate'] if img_element and 'loadlate' in img_element.attrs else 'N/A'
                    
                    # Extract rating
                    rating_element = card.find('div', class_='inline-block ratings-imdb-rating')
                    if rating_element:
                        rating_str = rating_element.find('strong').text.strip()
                        rating = float(rating_str)
                    else:
                        rating = None
                    
                    # Extract type/genre
                    genre_element = card.find('span', class_='genre')
                    movie_type = genre_element.text.strip() if genre_element else 'N/A'
                    
                    # Apply rating filter
                    if rating is not None and rating >= min_rating:
                        movies.append({
                            'name': name,
                            'image_url': image_url,
                            'rating': rating,
                            'type': movie_type
                        })
                        print(f"  ✓ {name} - Rating: {rating}")
                    elif rating is not None and min_rating > 0:
                        print(f"  ✗ {name} - Rating: {rating} (below threshold)")
                
                except Exception as e:
                    print(f"  ✗ Error parsing movie: {e}")
                    continue
            
            # Be respectful - add delay between requests
            if page < num_pages:
                time.sleep(1)
        
        except Exception as e:
            print(f"  ✗ Error scraping page {page}: {e}")
            continue
    
    # Sort by rating if requested
    if sort_by_rating and movies:
        movies = sorted(movies, key=lambda x: x['rating'] if x['rating'] else 0, reverse=True)
    
    return movies

def save_to_csv(movies, filename='movie.csv'):
    """Save movie data to CSV file."""
    df = pd.DataFrame(movies)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n✓ Saved {len(movies)} movies to {filename}")
    return df

def main():
    parser = argparse.ArgumentParser(description='Scrape movie data from IMDb')
    parser.add_argument('--pages', type=int, default=10, help='Number of pages to scrape (default: 10)')
    parser.add_argument('--min-rating', type=float, default=0.0, help='Minimum rating threshold (default: 0.0)')
    parser.add_argument('--sort', action='store_true', help='Sort by rating (highest first)')
    parser.add_argument('--output', type=str, default='movie.csv', help='Output CSV filename (default: movie.csv)')
    
    args = parser.parse_args()
    
    # Scrape movies
    movies = scrape_movies(
        num_pages=args.pages,
        min_rating=args.min_rating,
        sort_by_rating=args.sort
    )
    
    if movies:
        # Save to CSV
        df = save_to_csv(movies, args.output)
        
        # Display summary
        print(f"\n" + "=" * 60)
        print(f"Summary:")
        print(f"  Total movies: {len(movies)}")
        if df['rating'].notna().any():
            print(f"  Average rating: {df['rating'].mean():.2f}")
            print(f"  Highest rating: {df['rating'].max():.2f}")
            print(f"  Lowest rating: {df['rating'].min():.2f}")
        print(f"=" * 60)
    else:
        print("\n✗ No movies found!")

if __name__ == "__main__":
    main()
