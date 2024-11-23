from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.crew_manager import CrewManager

router = APIRouter()

class TweetAnalysisRequest(BaseModel):
    tweet_url: str

@router.post("/analyze")
async def analyze_tweet(request: TweetAnalysisRequest):
    try:
        crew_manager = CrewManager()
        result = crew_manager.analyze_tweet(request.tweet_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))