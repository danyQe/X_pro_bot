import { NextResponse } from "next/server";

// This is a mock API response. In production, this would call your Python backend
export async function POST(req: Request) {
  const body = await req.json();
  
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1500));

  // Mock response data
  const mockAnalysis = {
    factCheck: {
      score: 85,
      explanation: "The claims in this tweet are mostly accurate based on our analysis. Some minor details require clarification.",
      sources: [
        "Official government statistics (2023)",
        "Academic research paper by Smith et al. (2022)",
        "Industry report from Bloomberg"
      ]
    },
    sentiment: {
      score: 0.6,
      explanation: "The tweet expresses a predominantly positive sentiment with constructive undertones. The language used is professional and informative."
    },
    summary: {
      text: "This tweet discusses recent developments in artificial intelligence and its impact on social media verification systems.",
      keyPoints: [
        "Introduction of new AI verification methods",
        "Impact on social media credibility",
        "Future implications for content verification"
      ],
      topics: [
        "AI Technology",
        "Social Media",
        "Content Verification",
        "Digital Trust"
      ]
    }
  };

  return NextResponse.json(mockAnalysis);
}