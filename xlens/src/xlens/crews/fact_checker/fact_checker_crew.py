from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
load_dotenv()
import os
# Uncomment the following line to use an example of a custom tool
# from fact_checker.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from tools.X_api_controller import TwitterAPIController
x_tool=TwitterAPIController(
	consumer_key=os.getenv("X_API_KEY"),
 consumer_secret=os.getenv("X_API_KEY_SECRET"),
 access_token=os.getenv("X_ACCESS_TOKEN"),
 access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
)
@CrewBase
class FactCheckerCrew():
	"""FactChecker crew"""

	@agent
	def fact_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['fact_checker'],
			tools=[x_tool], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	# @agent
	# def reporting_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reporting_analyst'],
	# 		verbose=True
	# 	)

<<<<<<< Updated upstream
	@task
	def fact_check(self) -> Task:
		return Task(
			config=self.tasks_config['fact_checking_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the FactChecker crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
=======
    @crew
    def crew(self) -> Crew:
        """Creates the FactChecker crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
>>>>>>> Stashed changes
