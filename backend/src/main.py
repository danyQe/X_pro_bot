#!/usr/bin/env python
from random import randint
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from crews.fact_checker.fact_checker_crew import FactCheckerCrew
from crews.sentiment_analyzer.sentiment_analyzer_crew import SentimentAnalyzerCrew
from crews.viral_tweet_generator.viral_tweet_generator_crew import ViralTweetGeneratorCrew

app = FastAPI(title="XLENS", description="APP for X Sentiment Analysis, Fact Checking, and Viral Thread Generation")

# Serve static files (adjust path accordingly)
app.mount("/", StaticFiles(directory=r"C:\\Users\\admin\\Desktop\\Projects\\XLENS\\XLENS_TEST\\xlens\\static", html=True), name="static")

class sentimentstate(BaseModel):
    tweet: str = ""

class FactState(BaseModel):
    tweet: str = ""

# Workflow Classes
class SENTIMENTFlow(Flow[sentimentstate]):
    """
    Analyzes sentiment using SentimentAnalyzerCrew
    """
    @start()
    def do_Analysis(self):
        result = SentimentAnalyzerCrew().crew().kickoff(inputs={"tweet": self.state.tweet})
        return result.raw

class FACTFlow(Flow[FactState]):
    """
    Checks facts using FactCheckerCrew
    """
    @start()
    def check_facts(self):
        result = FactCheckerCrew().crew().kickoff(inputs={"tweet": self.state.tweet})
        return result.raw

class VIRALFlow(Flow):
    """
    Generates viral tweets using ViralTweetGeneratorCrew
    """
    @start()
    def create_viral_tweets(self):
        result = ViralTweetGeneratorCrew().crew().kickoff()
        return result.raw

# FastAPI Routes
@app.post("/sentiment")
async def sentiment_kickoff(data: sentimentstate):
    sentiment_flow = SENTIMENTFlow()
    return {"sentiment_description": sentiment_flow.kickoff()}

@app.post("/facts")
async def fact_kickoff(data: FactState):
    fact_flow = FACTFlow()
    return {"Fact_description": fact_flow.kickoff()}

@app.get("/viral")
def viraltweetkickoff():
    viral_flow = VIRALFlow()
    return {"viral_tweets": viral_flow.kickoff()}

# For local testing:
if __name__ == "__main__":
    result = SENTIMENTFlow().kickoff(inputs={"tweet": """Development wins!

    Good governance wins! 

    United we will soar even higher! 

    Heartfelt gratitude to my sisters and brothers of Maharashtra, especially the youth and women of the state, for a historic mandate to the NDA. This affection and warmth is unparalleled. 

    I assure the people that our Alliance will keep working for Maharashtra’s progress. 

    Jai Maharashtra!"""})
    print(result)
