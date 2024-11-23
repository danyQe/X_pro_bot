import requests
from bs4 import BeautifulSoup
from typing import Optional

class WebScraper:
    @staticmethod
    def scrape_tweet(url: str) -> Optional[dict]:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract tweet content (this is a simplified example)
            tweet_text = soup.find('div', {'data-testid': 'tweetText'})
            tweet_time = soup.find('time')
            
            return {
                'text': tweet_text.text if tweet_text else None,
                'timestamp': tweet_time['datetime'] if tweet_time else None,
            }
        except Exception as e:
            print(f"Error scraping tweet: {str(e)}")
            return None