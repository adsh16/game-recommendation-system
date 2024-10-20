"""
Using Steam.com to get reviews and number of reviews of the game
"""


# <span class="game_review_summary positive" data-tooltip-html="81% of the 57,209 user reviews for this game are positive.">Very Positive</span>

#  You can find the review summary in the span tag with the class game_review_summary
# it would be of this type
"""
Steam review system

95 - 100 | 500+ reviews | positive | overwhelming

85 - 100 | 50+ reviews | positive | very

80 - 100 | 1+ reviews | positive

70 - 79 | 1+ reviews | positive | mostly

40 - 69 | 1+ reviews | mixed

20 - 39 | 1+ reviews | negative | mostly

0 - 19 | 1+ reviews | negative

0 - 19 | 50+ reviews | negative | very

0 - 19 | 500+ reviews | negative | overwhelming
"""
"""
I have a csv file called games.csv with the following column
do not CHANGE anything in the files
create a dataframe and do changes in that
name
Galactic Bowling
TD Worlds

do what search on google <game name> steam
go on the steam page of the game
get the review summary and number of reviews
put it in the csv file
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

# Step 1: Load the CSV file
df = pd.read_csv('games.csv')

# Initialize lists to store the review summaries and counts
review_summaries = []
review_counts = []

# Function to fetch reviews from Steam
def fetch_reviews(game_name):
    # Step 2: Search for the game on Google
    search_query = urllib.parse.quote_plus(f"{game_name} steam")
    google_search_url = f"https://www.google.com/search?q={search_query}"
    
    # Get the Google search results
    response = requests.get(google_search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first result that likely points to the Steam page
    steam_url = None
    for link in soup.find_all('a'):
        href = link.get('href')
        if 'store.steampowered.com/app/' in href:
            steam_url = href.split('=')[1]  # Extract the Steam URL
            break

    if not steam_url:
        return None, None  # If no Steam page found

    # Step 3: Scrape the Steam page
    steam_response = requests.get(steam_url)
    steam_soup = BeautifulSoup(steam_response.text, 'html.parser')

    # Find the review summary and number of reviews
    review_summary = steam_soup.find('span', class_='game_review_summary')
    if review_summary:
        review_text = review_summary['data-tooltip-html']
        review_summary_text = review_text.split(' are ')[0]  # e.g., "81% of the 57,209 user reviews for this game"
        review_count = review_text.split(' user reviews for this game are ')[1].split('.')[0]
        
        review_counts.append(review_count)
        review_summaries.append(review_summary_text)
    else:
        review_summaries.append(None)
        review_counts.append(None)

    time.sleep(1)  # Sleep to avoid hitting the server too fast

# Step 4: Iterate through the DataFrame
for game_name in df['name']:
    fetch_reviews(game_name)

# Step 5: Add the results to the DataFrame
df['review_summary'] = review_summaries
df['review_count'] = review_counts

# Step 6: Save the updated DataFrame back to CSV
df.to_csv('games_with_reviews.csv', index=False)
