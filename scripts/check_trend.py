import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

try:
    from skills.trend_fetcher import TrendQuery, TrendResult, execute

    print("Imported skills.trend_fetcher successfully")
except Exception as e:
    print("Import failed:", type(e), e)
    raise


def try_create(*args, **kwargs):
    try:
        obj = TrendQuery(*args, **kwargs)
        print("Created TrendQuery for", args, kwargs, "->", obj)
    except Exception as e:
        print("Exception for", args, kwargs, "->", type(e), e)


try_create("")
try_create("AI", region="invalid-region!")
try_create("AI", timeframe_hours=200)
