#!/usr/bin/env python
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from crewai.flow.flow import Flow, start
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

class SENTIMENTFlow(Flow[SentimentState]):
    @start()
    def do_Analysis(self):
        global tweet
        inputs={"tweet":tweet}
        print("tweet recieved:",tweet)
        result = SentimentAnalyzerCrew().crew().kickoff(inputs=inputs)
        return result.raw

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
        result = ViralTweetGeneratorCrew().crew().kickoff()
        return result.raw

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
    return {"viral_tweets": viral_flow.kickoff()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)