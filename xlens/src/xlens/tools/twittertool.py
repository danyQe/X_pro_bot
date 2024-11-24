from crewai_tools import tool
import tweepy
import os
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class TwitterTool:
    """Twitter API tool for CrewAI agents"""
    
    def __init__(self):
        """Initialize Twitter API clients"""
        # Client for app-only authentication (trending topics)
        self.client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            wait_on_rate_limit=True
        )

    @tool("Tweet Publisher")
    def publish_tweet(self, text: str, reply_to_tweet_id: Optional[str] = None) -> Dict[str, Any]:
        """Publishes a tweet to Twitter/X
        
        Args:
            text: The text content of the tweet (max 280 characters)
            reply_to_tweet_id: Optional ID of tweet to reply to
        
        Returns:
            Dictionary containing tweet data including ID and text
        """
        try:
            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=reply_to_tweet_id
            )
            
            return {
                "success": True,
                "tweet_id": response.data["id"],
                "tweet_text": text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @tool("Trending Topics Analyzer")
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