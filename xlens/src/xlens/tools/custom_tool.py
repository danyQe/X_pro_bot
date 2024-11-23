from X_api_controller import TwitterAPIController
from crewai.tools import tool
from crewai.tools import BaseTool

class TwitterTool(BaseTool):
    name: str = "Twitter Tool"
    description: str = "A tool for interacting with Twitter: reading, replying, retweeting, and liking tweets."

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        super().__init__()
        self.twitter_controller = TwitterAPIController(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )

    def _run(self, action: str, tweet_id: int = None, content: str = None, query: str = None, count: int = 10) -> dict:
        return self.twitter_controller.control_twitter_api(
            action=action,
            tweet_id=tweet_id,
            content=content,
            query=query,
            count=count
        )

