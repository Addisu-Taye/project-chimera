def test_import_skills_module():
    import importlib
    m = importlib.import_module('skills.trend_fetcher')
    # ensure module has expected attributes
    assert hasattr(m, 'TrendQuery')
    assert hasattr(m, 'TrendResult')
    assert hasattr(m, 'execute')
    print('module file:', getattr(m, '__file__', None))
