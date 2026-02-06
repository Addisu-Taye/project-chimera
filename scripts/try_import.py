import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
try:
    m = importlib.import_module("skills.trend_fetcher")
    print("import ok:", m)
except Exception as e:
    print("import failed:", type(e), e)
    raise
