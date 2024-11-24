from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\HP\Desktop\PROJECTS\BUILDATHON\X_LENS_TEST\xlens\.env")
# Uncomment the following line to use an example of a custom tool
# from sentiment_analyzer.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool
llm=LLM(
	model="groq/llama-3.1-70b-versatile",
 api_key=os.getenv("GROQ_API_KEY"),
 temperature=0
)
@CrewBase
class SentimentAnalyzerCrew():
	"""SentimentAnalyzer crew"""

	@agent
	def analyzer(self) -> Agent:
		return Agent(
            llm=llm,
			config=self.agents_config['analyzer']
		)

	@task
	def analyze_Sentiment(self) -> Task:
		return Task(
			config=self.tasks_config['sentiment_analysis_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SentimentAnalyzer crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)