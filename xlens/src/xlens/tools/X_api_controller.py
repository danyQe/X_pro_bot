import tweepy

class TwitterAPIController:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Initialize the Twitter API controller.
        """
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def post_tweet(self, content):
        """
        Post a tweet using the Twitter API.
        
        Parameters:
        - content (str): The text content of the tweet to post
        
        Returns:
        - dict: The result of posting the tweet containing tweet ID and text
        """
        try:
            posted_tweet = self.api.update_status(status=content)
            return {
                "id": posted_tweet.id,
                "text": posted_tweet.text
            }
        except tweepy.TweepError as e:
            return {"error": str(e)}

    def search_tweets(self, query, count=10):
        """
        Search for tweets using the Twitter API.
        
        Parameters:
        - query (str): Search query for reading tweets
        - count (int): Number of tweets to fetch (default: 10)
        
        Returns:
        - list: List of tweets matching the search query
        """
        try:
            tweets = self.api.search_tweets(q=query, count=count, tweet_mode='extended')
            return tweets
        except tweepy.TweepError as e:
            return {"error": str(e)}
