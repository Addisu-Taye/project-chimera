"""
Test for skills interface contracts based on specs/technical.md §Skill Contract Pattern
SRS Trace: §4.6 Orchestration & Swarm Governance
These tests validate that implemented skills follow the required contract.
"""

import pytest
from pydantic import ValidationError
import inspect

# Test base skill contract pattern
def test_base_skill_input_contract():
    """Test that all skills follow BaseSkillInput pattern"""
    # Story: A rigorous gatekeeper inspects every skill input to ensure
    # it carries a clear reference to the spec that defined it.
    # This keeps the swarm auditable and maintainable.
    try:
        from skills.trend_fetcher import TrendQuery
        from skills.image_generator import ImageRequest
        from skills.wallet_manager import TransactionRequest
    except ImportError:
        pytest.skip("Skills not implemented yet - this is expected")
    
    # All skill inputs must have traceability fields
    for SkillInput in [TrendQuery, ImageRequest, TransactionRequest]:
        fields = SkillInput.model_fields  # Pydantic v2 uses model_fields
        
        # Must have spec_reference field
        assert 'spec_reference' in fields
        spec_ref_field = fields['spec_reference']
        assert spec_ref_field.annotation == str
        assert spec_ref_field.default is not None
        assert spec_ref_field.default.startswith('specs/')
        assert '§F-' in spec_ref_field.default
        
        # Must have srs_requirement field  
        assert 'srs_requirement' in fields
        srs_req_field = fields['srs_requirement']
        assert srs_req_field.annotation == str
        assert srs_req_field.default is not None
        assert srs_req_field.default.startswith('§')

def test_base_skill_output_contract():
    """Test that all skills follow BaseSkillOutput pattern"""
    # Story: Outputs must include confidence and timing so Judges can rate quality.
    try:
        from skills.trend_fetcher import TrendResult
        from skills.image_generator import ImageResult  
        from skills.wallet_manager import TransactionResult
    except ImportError:
        pytest.skip("Skills not implemented yet - this is expected")
    
    # All skill outputs must have required fields
    for SkillOutput in [TrendResult, ImageResult, TransactionResult]:
        fields = SkillOutput.model_fields  # Pydantic v2
        
        # Must have confidence_score
        assert 'confidence_score' in fields
        conf_field = fields['confidence_score']
        assert conf_field.annotation == float
        # Note: confidence_score should not have a default - it's computed at runtime
        
        # Must have execution_time_ms
        assert 'execution_time_ms' in fields
        time_field = fields['execution_time_ms']
        assert time_field.annotation == int
        
        # Must have spec_compliant
        assert 'spec_compliant' in fields
        compliant_field = fields['spec_compliant']
        assert compliant_field.annotation == bool
        assert compliant_field.default is True

def test_skill_execution_signature():
    """Test that all skills have async execute function with proper signature"""
    # Story: Skills are atomic capabilities; their execute signature must be
    # asynchronous and accept a single Pydantic model to fit the orchestration flow.
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
        
        # Parameter must be a Pydantic model (has model_fields attribute)
        param = list(sig.parameters.values())[0]
        param_type = param.annotation
        assert hasattr(param_type, 'model_fields')  # Pydantic v2 model check

def test_forbidden_patterns():
    """Ensure skills don't contain forbidden patterns"""
    # Story: Skills must stay pure — orchestration belongs in the Planner.
    # When implemented, this test will scan skill sources for forbidden constructs.
    pass  # Implementation will check source code for forbidden patterns