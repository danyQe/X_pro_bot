#!/usr/bin/env python
from random import randint
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from xlens.src.xlens.crews.fact_checker.fact_checker_crew import FactCheckerCrew
from xlens.src.xlens.crews.sentiment_analyzer.sentiment_analyzer_crew import SentimentAnalyzerCrew
from xlens.src.xlens.crews.viral_tweet_generator.viral_tweet_generator_crew import ViralTweetGeneratorCrew

app = FastAPI(title="XLENS", description="APP for X Sentiment Analysis, Fact Checking, and Viral Thread Generation")
app.mount("/",StaticFiles(directory=r"C:\Users\HP\Desktop\PROJECTS\BUILDATHON\X_LENS_TEST\xlens\static",html=True),name="static")
class sentimentstate(BaseModel):
    tweet:str=""
class FactState(BaseModel):
    tweet:str=""

class SENTIMENTFlow(Flow[sentimentstate]):
    @start()
    def do_Analysis(self):
        result=SentimentAnalyzerCrew().crew().kickoff(inputs={"tweet":self.state.tweet})
        return result.raw
class FACTFlow(Flow[FactState]):
     @start()
     def check_facts(self):
         result=FactCheckerCrew().crew().kickoff(inputs={"tweet":self.state.tweet})
         return result.raw
class VIRALFlow(Flow):
      @start()
      def create_viral_tweets(self):
          result=ViralTweetGeneratorCrew().crew().kickoff()
          return result.raw
@app.post("/sentiment")
async def sentiment_kickoff(data:sentimentstate):
    sentiment_flow = SENTIMENTFlow()
    return {"sentiment_description":sentiment_flow.kickoff()}
@app.post("/facts")
async def fact_kickoff(data:FactState):
    fact_flow = FACTFlow()
    return {"Fact_description":fact_flow.kickoff()}
@app.get("/viral")
def  viraltweetkickoff():
     viral_flow=VIRALFlow()
     return {"viral_tweets":viral_flow.kickoff()}
if __name__ == "__main__":
    result=SENTIMENTFlow().kickoff(inputs={"tweet":"""Development wins!

Good governance wins! 

United we will soar even higher! 

Heartfelt gratitude to my sisters and brothers of Maharashtra, especially the youth and women of the state, for a historic mandate to the NDA. This affection and warmth is unparalleled. 

I assure the people that our Alliance will keep working for Maharashtra’s progress. 

Jai Maharashtra!"""})
    print(result)