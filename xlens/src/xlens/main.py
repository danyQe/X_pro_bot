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

class SentimentState(BaseModel):
    tweet: str

class FactState(BaseModel):
    tweet: str = ""

class SENTIMENTFlow(Flow[SentimentState]):
    @start()
    def do_Analysis(self):
        result = SentimentAnalyzerCrew().crew().kickoff()
        return result.raw

class FACTFlow(Flow[FactState]):
    @start()
    def check_facts(self):
        result = FactCheckerCrew().crew().kickoff()
        return result.raw

class VIRALFlow(Flow):
    @start()
    def create_viral_tweets(self):
        result = ViralTweetGeneratorCrew().crew().kickoff()
        return result.raw

@app.post("/sentiment")
async def sentiment_kickoff(data: SentimentState):
    try:
        sentiment_flow = SENTIMENTFlow()
        sentiment_description = sentiment_flow.kickoff({"tweet": data.tweet})
        result = sentiment_description
        return {"sentiment_description": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/facts")
async def fact_kickoff(data: FactState):
    fact_flow = FACTFlow()
    fact_description = fact_flow.kickoff(inputs={"tweet": data.tweet})
    return {"Fact_description": fact_description}

@app.get("/viral")
def viraltweetkickoff():
    viral_flow = VIRALFlow()
    return {"viral_tweets": viral_flow.kickoff()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)