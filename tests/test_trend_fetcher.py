"""
Test for trend_fetcher skill based on specs/technical.md §Agent Task Schema
SRS Trace: §4.2 FR 2.2
These tests SHOULD FAIL until the skill is implemented.
"""

import pytest
from pydantic import ValidationError
from unittest.mock import AsyncMock

# Import will fail until skill is implemented - this is EXPECTED
try:
    from skills.trend_fetcher import TrendQuery, TrendResult, execute
except ImportError:
    # Define minimal contracts to validate structure
    class TrendQuery:
        def __init__(self, topic, region="global", timeframe_hours=24):
            self.topic = topic
            self.region = region
            self.timeframe_hours = timeframe_hours
    
    class TrendResult:
        def __init__(self, trends, relevance_score):
            self.trends = trends
            self.relevance_score = relevance_score

def test_trend_query_validation():
    """Test TrendQuery input validation per specs/functional.md §F-002"""
    # Should fail - empty topic
    with pytest.raises((ValidationError, ValueError)):
        TrendQuery("")
    
    # Should fail - invalid region format
    with pytest.raises((ValidationError, ValueError)):
        TrendQuery("AI", region="invalid-region!")
    
    # Should fail - timeframe out of bounds
    with pytest.raises((ValidationError, ValueError)):
        TrendQuery("AI", timeframe_hours=200)  # > 168 hours
    
    # Should pass - valid input
    query = TrendQuery("AI agents", "us_west", 48)
    assert query.topic == "AI agents"
    assert query.region == "us_west"
    assert query.timeframe_hours == 48

def test_trend_result_validation():
    """Test TrendResult output validation per specs/functional.md §F-002"""
    # Should fail - relevance_score out of bounds
    with pytest.raises((ValidationError, ValueError)):
        TrendResult(["trend1"], 1.5)  # > 1.0
    
    with pytest.raises((ValidationError, ValueError)):
        TrendResult(["trend1"], -0.1)  # < 0.0
    
    # Should fail - empty trends
    with pytest.raises((ValidationError, ValueError)):
        TrendResult([], 0.8)
    
    # Should pass - valid output
    result = TrendResult(["AI agents", "autonomous influencers"], 0.85)
    assert len(result.trends) == 2
    assert result.relevance_score == 0.85

@pytest.mark.asyncio
async def test_trend_fetcher_execution_contract():
    """Test that execute function follows the required contract"""
    # This will fail until the skill is implemented
    query = TrendQuery("AI", "global", 24)
    
    # Should return TrendResult with confidence_score and execution_time_ms
    result = await execute(query)
    
    # Validate required fields from specs/technical.md §Skill Contract Pattern
    assert hasattr(result, 'confidence_score')
    assert hasattr(result, 'execution_time_ms')
    assert hasattr(result, 'spec_compliant')
    assert 0.0 <= result.confidence_score <= 1.0
    assert result.execution_time_ms >= 0

def test_spec_traceability():
    """Verify spec traceability requirements are met"""
    # Every skill must reference specs and SRS
    query = TrendQuery("test", "global", 24)
    
    # Check for required traceability fields
    assert hasattr(query, 'spec_reference')
    assert hasattr(query, 'srs_requirement')
    assert query.spec_reference == "specs/functional.md §F-002"
    assert query.srs_requirement == "§4.2 FR 2.2"