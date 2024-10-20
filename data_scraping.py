import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import re
import os
import random

# Function to load user agents from user_agents.txt
def load_user_agents(file_path):
    with open(file_path, 'r') as file:
        user_agents = [line.strip() for line in file if line.strip()]
    return user_agents

user_agents = load_user_agents('user_agents.txt')

def get_random_user_agent(user_agents):
    """Returns a random user agent string from the list."""
    return random.choice(user_agents)

def get_steam_url(game_name):
    """Search for the game on Google and return its Steam URL."""
    headers = {
        'User-Agent': get_random_user_agent(user_agents)
    }
    
    search_query = urllib.parse.quote_plus(f"{game_name} steam store")
    google_search_url = f"https://www.google.com/search?q={search_query}"
    
    try:
        response = requests.get(google_search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = str(link.get('href'))
            if 'store.steampowered.com/app/' in href:
                try:
                    steam_url = href.split('&')[0].split('=')[1]
                    return steam_url
                except IndexError:
                    match = re.search(r'store\.steampowered\.com/app/\d+', href)
                    if match:
                        return 'https://' + match.group(0)
                    continue
        
        print(f"No Steam store page found for {game_name}")
        return None
        
    except Exception as e:
        print(f"Error searching for {game_name}: {str(e)}")
        return None

def fetch_game_data(game_name):
    """Fetch review data and image for a given game from Steam."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    steam_url = get_steam_url(game_name)
    if not steam_url:
        return "Not found", 0, 0, None
    
    try:
        response = requests.get(steam_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get review count
        review_count_meta = soup.find('meta', {'itemprop': 'reviewCount'})
        review_count = int(review_count_meta['content']) if review_count_meta else 0
        
        # Get review rating
        review_desc = soup.find('span', class_='responsive_reviewdesc')
        if review_desc:
            rating_match = re.search(r'(\d+)%', review_desc.text)
            review_rating = int(rating_match.group(1)) if rating_match else 0
        else:
            review_rating = 0
        
        # Get review summary
        review_summary = soup.find('span', class_='game_review_summary')
        review_summary = review_summary.text.strip() if review_summary else "No reviews"
        
        # Get game header image
        header_img = soup.find('img', class_='game_header_image_full')
        image_link = header_img['src'] if header_img else None
        
        return review_summary, review_count, review_rating, image_link
        
    except Exception as e:
        print(f"Error fetching data for {game_name} from {steam_url}: {str(e)}")
        return "Error", 0, 0, None

def main():
    # Read the CSV file
    try:
        df = pd.read_csv('games.csv')
        
        # File path for the output CSV
        output_file = 'games_with_reviews.csv'
        
        # Check if file already exists (for appending mode)
        file_exists = os.path.isfile(output_file)
        
        # Process each game
        for idx, game_name in enumerate(df['name']):
            print(f"Processing {game_name} {idx}...")
            
            # Get game data
            data = fetch_game_data(game_name)
            if data is None:
                data = ("Error", 0, 0, None)
                
            review_summary, review_count, review_rating, image_link = data
            
            # Create a DataFrame for the current game
            game_data_df = pd.DataFrame({
                'name': [game_name],
                'review_summary': [review_summary],
                'review_count': [review_count],
                'review_rating': [review_rating],
                'image_link': [image_link]
            })
            
            # Append data to CSV
            game_data_df.to_csv(output_file, mode='a', header=not file_exists, index=False)
            
            # Set file_exists to True after the first append
            file_exists = True
            
            # Optional: Add a delay to avoid overwhelming the server
            # 1-3 seconds is a good range
            time.sleep(random.uniform(1, 3))
        
        print("Processing complete! Data saved to games_with_reviews.csv")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
