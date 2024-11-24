from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from tools.googletrends import GoogleTrendsTool
from tools.twittertool import TwitterTool
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize LLM
llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# Initialize tools


@CrewBase
class ViralTweetGeneratorCrew():
    """ViralTweetGenerator crew"""

    @agent
    def content_researcher(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['researcher'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), GoogleTrendsTool().analyze_interest_by_region,GoogleTrendsTool().analyze_interest_by_region],
            verbose=True,
            allow_delegation=True
        )

    @agent
    def tweet_writer(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['tweet_writer'],
            tools=[TwitterTool().publish_tweet],
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
            agent=self.tweet_writer()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ViralTweetGenerator crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )