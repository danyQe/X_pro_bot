from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool,TXTSearchTool,FileReadTool
from xlens.src.xlens.tools.googletrends import GoogleTrendsTool
# from tools.twittertool import TwitterTool
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()
google_trends=GoogleTrendsTool()
class Tweet(BaseModel):
    tweet: List[str]

# Initialize LLM
llm = LLM(
    model="gemini/gemini-1.5-flash", 
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

@CrewBase
class ViralTweetGeneratorCrew():
    """ViralTweetGenerator crew"""

    @agent
    def content_researcher(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['researcher'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), google_trends.analyze_interest_by_region],
            verbose=True,
            allow_delegation=True
        )

    @agent 
    def tweet_writer(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['tweet_writer'],
            verbose=True
        )

    @task
    def content_research(self) -> Task:
        return Task(
            config=self.tasks_config['viral_content_research'],
            agent=self.content_researcher()
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['viral_content_tweet'],
            agent=self.tweet_writer(),
            tools=[TXTSearchTool(),FileReadTool(r"C:\Users\HP\Desktop\PROJECTS\BUILDATHON\X_LENS_TEST\tweet.txt")],
            output_pydantic=Tweet,
            output_file="tweet.txt"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ViralTweetGenerator crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder={
                "provider": "google",
                "config": {
                    "api_key": os.getenv("GEMINI_API_KEY"),
                    "model": "models/text-embedding-004"
                }
            }
        )