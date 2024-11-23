import tweepy
class TwitterAPIController:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Initialize the Twitter API controller.
        """
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def control_twitter_api(self, action, tweet_id=None, content=None, query=None, count=10):
        """
        Perform actions on the Twitter API based on the given parameters.
        
        Parameters:
        - action (str): The action to perform ('read', 'reply', 'retweet', 'like').
        - tweet_id (int): The ID of the tweet (required for 'reply', 'retweet', 'like').
        - content (str): The content for the reply (required for 'reply').
        - query (str): Search query for reading tweets (required for 'read').
        - count (int): Number of tweets to fetch (default: 10).
        
        Returns:
        - dict or list: The result of the action performed.
        """
        try:
            if action == 'read':
                if not query:
                    raise ValueError("Query is required for reading tweets.")
                tweets = self.api.search_tweets(q=query, count=count, tweet_mode='extended')
                return [{"id": tweet.id, "user": tweet.user.screen_name, "text": tweet.full_text} for tweet in tweets]

            elif action == 'reply':
                if not tweet_id or not content:
                    raise ValueError("Tweet ID and content are required for replying.")
                reply_tweet = self.api.update_status(status=content, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
                return {"id": reply_tweet.id, "text": reply_tweet.text}

            elif action == 'retweet':
                if not tweet_id:
                    raise ValueError("Tweet ID is required for retweeting.")
                retweet = self.api.retweet(tweet_id)
                return {"id": retweet.id, "text": retweet.text}

            elif action == 'like':
                if not tweet_id:
                    raise ValueError("Tweet ID is required for liking a tweet.")
                self.api.create_favorite(tweet_id)
                return {"status": "liked", "tweet_id": tweet_id}

            else:
                raise ValueError("Unsupported action. Use 'read', 'reply', 'retweet', or 'like'.")

        except tweepy.TweepError as e:
            return {"error": str(e)}

