#!/usr/bin/env python
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from xlens.src.xlens.tools.twittertool import TwitterTool
from crewai.flow.flow import Flow, start,listen
from xlens.src.xlens.crews.fact_checker.fact_checker_crew import FactCheckerCrew
from xlens.src.xlens.crews.sentiment_analyzer.sentiment_analyzer_crew import SentimentAnalyzerCrew
from xlens.src.xlens.crews.viral_tweet_generator.viral_tweet_generator_crew import ViralTweetGeneratorCrew

app = FastAPI(title="XLENS", description="APP for X Sentiment Analysis, Fact Checking, and Viral Thread Generation")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
tweet=""
class SentimentState(BaseModel):
    tweet: str=""

class FactState(BaseModel):
    tweet: str = ""
class TweetRequest(BaseModel):
    tweet: str
class SENTIMENTFlow(Flow[SentimentState]):
    @start()
    def do_Analysis(self):
        global tweet
        inputs={"tweet":tweet}
        print("tweet recieved:",tweet)
        result = SentimentAnalyzerCrew().crew().kickoff(inputs=inputs)
        Tweet=result.pydantic
        return Tweet.tweet[0]

class FACTFlow(Flow[FactState]):
    @start()
    def check_facts(self):
        global tweet
        inputs = {"tweet": tweet}
        print(f"Processing tweet: {tweet}")
        result = FactCheckerCrew().crew().kickoff(inputs=inputs)
        return result.raw

class VIRALFlow(Flow):
    @start()
    def create_viral_tweets(self):
        result = ViralTweetGeneratorCrew().crew().kickoff().pydantic
        return result
    @listen("create_viral_tweets")
    def listen_viral_tweets(self,result):
        tweets=[]
        print("viral tweets recieved:",result)
        for i,tweet in enumerate(result.tweet):
            print(f"tweet{i}:{tweet}")
            tweets.append(tweet)
        return tweets
@app.post("/sentiment")
def sentiment_kickoff(data: SentimentState):
    print("tweet recieved:",data.tweet)
    global tweet
    tweet=data.tweet
    sentiment_flow = SENTIMENTFlow()
    return {"sentiment_description": sentiment_flow.kickoff()}

@app.post("/facts")
def fact_kickoff(data: FactState):
    fact_flow = FACTFlow()
    print(f"Received tweet: {data.tweet}")
    global tweet
    tweet=data.tweet
    return {"Fact_description": fact_flow.kickoff()}

@app.get("/viral")
def viral_tweet_kickoff():
    viral_flow = VIRALFlow()
    result=viral_flow.kickoff()
    return {"viral_tweets": result if result else []}
@app.post("/tweet")
async def tweet(request: TweetRequest):
    try:
        if not request.tweet:
            raise HTTPException(status_code=400, detail="Tweet text cannot be empty")

        twitter_tool = TwitterTool()
        result = twitter_tool.post_tweet(request.tweet)
        print(f"Tweet result: {result}")  # Debug logging
        
        if isinstance(result, dict) and result.get("success"):
            tweet_data = result["data"].data  # Access the nested data
            return {
                "message": "Tweet published successfully!",
                "tweet_id": tweet_data["id"],
                "tweet_text": tweet_data["text"]
            }
        else:
            print(f"Failed result: {result}")
            raise HTTPException(
                status_code=500, 
                detail=result.get("error", "Failed to publish tweet")
            )
    except HTTPException as he:
        print(f"HTTP error: {str(he)}")
        raise
    except Exception as e:
        print(f"Tweet error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to publish tweet: {str(e)}"
        )
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)