from typing import List, Dict, Any
from crewai_tools import tool
from pytrends.request import TrendReq
import pandas as pd

class GoogleTrendsTool:
    """Google Trends tool for CrewAI agents"""
    
    def __init__(self):
        """Initialize Google Trends client"""
        self.pytrends = TrendReq(hl="en-US", tz=360)

    @tool("Interest Over Time Analyzer")
    def analyze_interest_over_time(
        self, 
        keywords: List[str], 
        timeframe: str = "today 5-y", 
        geo: str = "", 
        category: int = 0
    ) -> Dict[str, Any]:
        """Analyzes interest over time for specified keywords
        
        Args:
            keywords: List of keywords to analyze (max 5 keywords)
            timeframe: Time frame for analysis. Options:
                - 'today 5-y' (last 5 years)
                - 'today 3-m' (last 3 months) 
                - 'now 7-d' (last 7 days)
                - 'now 4-H' (last 4 hours)
                - Or specific dates: 'YYYY-MM-DD YYYY-MM-DD'
            geo: Geographic location code (e.g., 'US' for United States)
            category: Category ID to filter results (default: 0 for all categories)
        
        Returns:
            Dictionary containing interest over time data, related topics and queries
        """
        try:
            # Build payload for Google Trends request
            self.pytrends.build_payload(
                kw_list=keywords[:5],  # Google Trends limits to 5 keywords
                cat=category,
                timeframe=timeframe,
                geo=geo
            )
            
            # Get interest over time data
            interest_data = self.pytrends.interest_over_time()
            
            # Get related topics and queries
            topics_data = self.pytrends.related_topics()
            queries_data = self.pytrends.related_queries()
            
            return {
                "success": True,
                "interest_over_time": interest_data.to_dict() if not interest_data.empty else {},
                "related_topics": {k: v.to_dict() if isinstance(v, pd.DataFrame) else v 
                                 for k, v in topics_data.items()},
                "related_queries": {k: {t: q.to_dict() if isinstance(q, pd.DataFrame) else q 
                                      for t, q in v.items()}
                                  for k, v in queries_data.items()}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @tool("Regional Interest Analyzer")  
    def analyze_interest_by_region(
        self,
        keywords: List[str],
        resolution: str = "COUNTRY",
        geo: str = "",
        timeframe: str = "today 12-m"
    ) -> Dict[str, Any]:
        """Analyzes interest by geographical region
        
        Args:
            keywords: List of keywords to analyze (max 5 keywords)
            resolution: Geographic resolution ('COUNTRY', 'REGION', 'CITY', 'DMA')
            geo: Geographic location to focus on (e.g., 'US' for United States)
            timeframe: Time frame for analysis
            
        Returns:
            Dictionary containing interest by region data
        """
        try:
            self.pytrends.build_payload(
                kw_list=keywords[:5],
                timeframe=timeframe,
                geo=geo
            )
            
            region_data = self.pytrends.interest_by_region(
                resolution=resolution,
                inc_low_vol=True,
                inc_geo_code=True
            )
            
            return {
                "success": True,
                "interest_by_region": region_data.to_dict()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
