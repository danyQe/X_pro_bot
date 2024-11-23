from crewai import Agent, Task, Crew
# from langchain_openai import ChatOpenAI
from config.settings import OPENAI_API_KEY
import os
from  langchain_groq import ChatGroq
class CrewManager:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.7,
            api_key=OPENAI_API_KEY
        )

    def analyze_tweet(self, tweet_url):
        # Create specialized agents
        fact_checker = Agent(
            role='Fact Checker',
            goal='Verify the accuracy of claims in tweets',
            backstory='Expert in fact-checking and verification with extensive research experience',
            llm=self.llm,
            tools=[],  # Add custom tools as needed
            verbose=True
        )

        sentiment_analyzer = Agent(
            role='Sentiment Analyzer',
            goal='Analyze the emotional tone and sentiment of tweets',
            backstory='Specialist in sentiment analysis and emotional intelligence',
            llm=self.llm,
            tools=[],
            verbose=True
        )

        summarizer = Agent(
            role='Content Summarizer',
            goal='Create concise, accurate summaries of tweet content',
            backstory='Expert in content analysis and summarization',
            llm=self.llm,
            tools=[],
            verbose=True
        )

        # Define tasks for each agent
        fact_check_task = Task(
            description=f"Analyze the tweet at {tweet_url} for factual accuracy",
            agent=fact_checker
        )

        sentiment_task = Task(
            description=f"Analyze the sentiment and emotional tone of the tweet at {tweet_url}",
            agent=sentiment_analyzer
        )

        summary_task = Task(
            description=f"Create a comprehensive summary of the tweet at {tweet_url}",
            agent=summarizer
        )

        # Create and run the crew
        crew = Crew(
            agents=[fact_checker, sentiment_analyzer, summarizer],
            tasks=[fact_check_task, sentiment_task, summary_task],
            verbose=True
        )

        result = crew.kickoff()

        # Process and structure the results
        return {
            "factCheck": {
                "score": 85,  # This would be calculated based on the actual analysis
                "explanation": result.get("fact_check", "Analysis not available"),
                "sources": [
                    "Official documentation",
                    "Verified news sources",
                    "Academic papers"
                ]
            },
            "sentiment": {
                "score": 0.6,  # This would be calculated based on the actual analysis
                "explanation": result.get("sentiment", "Analysis not available")
            },
            "summary": {
                "text": result.get("summary", "Summary not available"),
                "keyPoints": [
                    "Main point 1",
                    "Main point 2",
                    "Main point 3"
                ],
                "topics": [
                    "Topic 1",
                    "Topic 2",
                    "Topic 3"
                ]
            }
        }