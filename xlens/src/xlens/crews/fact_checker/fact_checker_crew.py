from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
# from tools.twittertool import TwitterTool
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

@CrewBase
class FactCheckerCrew():
    """FactChecker crew"""

    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['fact_checker'],
            tools=[SerperDevTool()],
            verbose=True,
            max_iter=2
        )

    @task
    def fact_check(self) -> Task:
        return Task(
            config=self.tasks_config['fact_checking_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FactChecker crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )