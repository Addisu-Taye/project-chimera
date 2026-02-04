import pytest 
from skills.skill_fetch_trends import fetch_trends 
def test_trend_fetcher(): 
    trends = fetch_trends("twitter") 
    assert isinstance(trends, list), "Trends should be a list" 
