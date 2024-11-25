from crewai_tools import BaseTool
import tweepy
import os
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class TwitterTool:
    name: str = "Twitter Tool"
    description: str = "Tool for interacting with Twitter API"

    def __init__(self):
        """Initialize Twitter API client with v2 endpoints"""
        super().__init__()
        
        # Load environment variables with exact names matching Twitter's documentation
        required_credentials = {
            "X_BEARER_TOKEN": os.getenv("X_BEARER_TOKEN"),
            "X_API_KEY": os.getenv("X_API_KEY"),
            "X_API_KEY_SECRET": os.getenv("X_API_KEY_SECRET"),
            "X_ACCESS_TOKEN": os.getenv("X_ACCESS_TOKEN"),
            "X_ACCESS_TOKEN_SECRET": os.getenv("X_ACCESS_TOKEN_SECRET")
        }
        
        missing_credentials = [key for key, value in required_credentials.items() if not value]
        if missing_credentials:
            raise ValueError(f"Missing required Twitter credentials: {', '.join(missing_credentials)}")

        try:
            # Initialize v2 Client with proper credential names
            self.client = tweepy.Client(
                bearer_token=required_credentials["X_BEARER_TOKEN"],
                consumer_key=required_credentials["X_API_KEY"],
                consumer_secret=required_credentials["X_API_KEY_SECRET"],
                access_token=required_credentials["X_ACCESS_TOKEN"],
                access_token_secret=required_credentials["X_ACCESS_TOKEN_SECRET"],
                wait_on_rate_limit=True
            )
            if not self.client:
                raise Exception("Failed to initialize Twitter client")
        except Exception as e:
            print(f"Error initializing Twitter client: {str(e)}")
            raise

    def post_tweet(self, text: str) -> dict:
        """
        Post a tweet using Twitter API v2
        Args:
            text (str): The text content of the tweet
        Returns:
            dict: Response containing success status and data/error
        """
        try:
            # Use v2 create_tweet method
            response = self.client.create_tweet(text=text)
            return {
                "success": True,
                "data": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Twitter API error: {str(e)}"
            }

    def analyze_trends(self, woeid: int = 1, exclude_hashtags: bool = False) -> Dict[str, Any]:
        """Gets trending topics for a specific location
        
        Args:
            woeid: The Yahoo! Where On Earth ID of the location (default: 1 for global)
            exclude_hashtags: Whether to exclude hashtags from results
        
        Returns:
            Dictionary containing trending topics data
        """
        try:
            # Get trending topics using Twitter API v2
            response = self.client.get_place_trends(
                id=woeid,
                exclude="hashtags" if exclude_hashtags else None
            )
            
            # Process trends data
            trends_data = []
            for trend in response[0]["trends"]:
                trend_info = {
                    "name": trend["name"],
                    "url": trend["url"],
                    "tweet_volume": trend["tweet_volume"] or 0,
                    "is_hashtag": trend["name"].startswith("#")
                }
                trends_data.append(trend_info)
            
            return {
                "success": True,
                "location_woeid": woeid,
                "trends": trends_data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }