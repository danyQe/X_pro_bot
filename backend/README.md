# Truth Terminal Backend

This is the backend service for Truth Terminal, an AI-powered Twitter analysis platform.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Update the `.env` file with your API keys and configuration.

5. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### POST /api/analyze
Analyzes a tweet for fact-checking, sentiment, and summary.

Request body:
```json
{
  "tweet_url": "https://twitter.com/example/status/123"
}
```

Response:
```json
{
  "factCheck": {
    "score": 85,
    "explanation": "...",
    "sources": [...]
  },
  "sentiment": {
    "score": 0.6,
    "explanation": "..."
  },
  "summary": {
    "text": "...",
    "keyPoints": [...],
    "topics": [...]
  }
}
```