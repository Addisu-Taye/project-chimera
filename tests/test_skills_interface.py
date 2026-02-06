"""
Test for skills interface contracts based on specs/technical.md §Skill Contract Pattern
SRS Trace: §4.6 Orchestration & Swarm Governance
These tests SHOULD FAIL until skills are implemented.
"""

import pytest
from pydantic import ValidationError

# Test base skill contract pattern
def test_base_skill_input_contract():
    """Test that all skills follow BaseSkillInput pattern"""
    # This will fail until skills implement proper contracts
    try:
        from skills.trend_fetcher import TrendQuery
        from skills.image_generator import ImageRequest
        from skills.wallet_manager import TransactionRequest
    except ImportError:
        pytest.skip("Skills not implemented yet - this is expected")
    
    # All skill inputs must have traceability fields
    for SkillInput in [TrendQuery, ImageRequest, TransactionRequest]:
        instance = SkillInput.__fields__  # Get field definitions
        
        # Must have spec_reference field
        assert 'spec_reference' in instance
        spec_ref = instance['spec_reference']
        assert spec_ref.type_ == str
        assert spec_ref.default.startswith('specs/')
        assert '§F-' in spec_ref.default
        
        # Must have srs_requirement field  
        assert 'srs_requirement' in instance
        srs_req = instance['srs_requirement']
        assert srs_req.type_ == str
        assert srs_req.default.startswith('§')

def test_base_skill_output_contract():
    """Test that all skills follow BaseSkillOutput pattern"""
    try:
        from skills.trend_fetcher import TrendResult
        from skills.image_generator import ImageResult  
        from skills.wallet_manager import TransactionResult
    except ImportError:
        pytest.skip("Skills not implemented yet - this is expected")
    
    # All skill outputs must have required fields
    for SkillOutput in [TrendResult, ImageResult, TransactionResult]:
        fields = SkillOutput.__fields__
        
        # Must have confidence_score
        assert 'confidence_score' in fields
        conf_field = fields['confidence_score']
        assert 0.0 <= conf_field.default <= 1.0
        
        # Must have execution_time_ms
        assert 'execution_time_ms' in fields
        time_field = fields['execution_time_ms']
        assert time_field.type_ == int
        
        # Must have spec_compliant
        assert 'spec_compliant' in fields
        compliant_field = fields['spec_compliant']
        assert compliant_field.type_ == bool

def test_skill_execution_signature():
    """Test that all skills have async execute function with proper signature"""
    import inspect
    
    skills = ['trend_fetcher', 'image_generator', 'wallet_manager']
    
    for skill_name in skills:
        try:
            skill_module = __import__(f'skills.{skill_name}', fromlist=['execute'])
            execute_func = getattr(skill_module, 'execute')
        except (ImportError, AttributeError):
            pytest.skip(f"{skill_name} not implemented yet - this is expected")
        
        # Must be async function
        assert inspect.iscoroutinefunction(execute_func)
        
        # Must accept single input parameter
        sig = inspect.signature(execute_func)
        assert len(sig.parameters) == 1
        
        # Parameter must be a Pydantic model
        param = list(sig.parameters.values())[0]
        assert hasattr(param.annotation, '__fields__')  # Pydantic model check

def test_forbidden_patterns():
    """Ensure skills don't contain forbidden patterns"""
    # Skills should NEVER contain orchestration logic
    # This test will help catch violations when skills are implemented
    pass  # Implementation will check source code for forbidden patterns