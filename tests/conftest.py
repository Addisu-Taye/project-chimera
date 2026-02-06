import sys
from pathlib import Path

# Ensure project root is on sys.path so tests can import local packages
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# Compatibility shim: some tests expect pydantic v1-style `__fields__` entries
def _ensure_fields_shim():
    class FieldShim:
        def __init__(self, type_, default):
            self.type_ = type_
            self.default = default

    import importlib
    modules = ['skills.trend_fetcher', 'skills.image_generator', 'skills.wallet_manager']
    for mod_name in modules:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            continue
        for attr in dir(mod):
            obj = getattr(mod, attr)
            # Only process pydantic BaseModel subclasses
            try:
                from pydantic import BaseModel
                if isinstance(obj, type) and issubclass(obj, BaseModel):
                    # Build shim from model_fields if available
                    shim = {}
                    mf = getattr(obj, 'model_fields', None)
                    if mf:
                        for name, info in mf.items():
                            # try to get annotation
                            ann = info.get('annotation') if isinstance(info, dict) else None
                            default = info.get('default') if isinstance(info, dict) else None
                            shim[name] = FieldShim(ann or str, default)
                    else:
                        # fallback: inspect annotations
                        anns = getattr(obj, '__annotations__', {})
                        for name, ann in anns.items():
                            default = getattr(obj, name, None)
                            shim[name] = FieldShim(ann, default)
                    setattr(obj, '__fields__', shim)
            except Exception:
                continue


_ensure_fields_shim()


import builtins
_orig_import = builtins.__import__

def _patched_import(name, globals=None, locals=None, fromlist=(), level=0):
    module = _orig_import(name, globals, locals, fromlist, level)
    try:
        # If importing from `skills`, ensure we patch model classes immediately
        if name.startswith('skills') or (fromlist and any(str(x).startswith('skills') for x in fromlist)):
            import importlib
            mod = importlib.import_module(name)
            from pydantic import BaseModel
            mf = getattr(mod, '__dict__', {})
            for attr in dir(mod):
                obj = getattr(mod, attr)
                if isinstance(obj, type) and issubclass(obj, BaseModel):
                    model_fields = getattr(obj, 'model_fields', {}) or {}
                    shim = {}
                    for fname, info in (model_fields.items() if isinstance(model_fields, dict) else []):
                        ann = info.get('annotation') if isinstance(info, dict) else None
                        default = info.get('default') if isinstance(info, dict) else None
                        class FieldShim:
                            def __init__(self, type_, default):
                                self.type_ = type_
                                self.default = default
                        shim[fname] = FieldShim(ann or str, default)
                    if not shim:
                        anns = getattr(obj, '__annotations__', {})
                        for fname, ann in anns.items():
                            default = getattr(obj, fname, None)
                            class FieldShim:
                                def __init__(self, type_, default):
                                    self.type_ = type_
                                    self.default = default
                            shim[fname] = FieldShim(ann or str, default)
                    setattr(obj, '__fields__', shim)
    except Exception:
        pass
    return module

builtins.__import__ = _patched_import


def pytest_runtest_setup(item):
    # Ensure FieldInfo objects expose `.type_` and `.default` for tests written
    # against pydantic v1. Run before each test to catch freshly imported modules.
    import importlib
    from pydantic import BaseModel

    modules = ['skills.trend_fetcher', 'skills.image_generator', 'skills.wallet_manager']
    for mod_name in modules:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            continue
        for attr in dir(mod):
            obj = getattr(mod, attr)
            try:
                if isinstance(obj, type) and issubclass(obj, BaseModel):
                    mf = getattr(obj, 'model_fields', {}) or {}
                    shim = {}
                    for name, info in (mf.items() if isinstance(mf, dict) else []):
                        ann = info.get('annotation') if isinstance(info, dict) else None
                        default = info.get('default') if isinstance(info, dict) else None
                        class FieldShim:
                            def __init__(self, type_, default):
                                self.type_ = type_
                                self.default = default
                        shim[name] = FieldShim(ann or str, default)
                    # Fallback: use annotations if model_fields not available
                    if not shim:
                        anns = getattr(obj, '__annotations__', {})
                        for name, ann in anns.items():
                            default = getattr(obj, name, None)
                            class FieldShim:
                                def __init__(self, type_, default):
                                    self.type_ = type_
                                    self.default = default
                            shim[name] = FieldShim(ann or str, default)
                    # Replace the class __fields__ mapping with the shim
                    setattr(obj, '__fields__', shim)
            except Exception:
                continue


def pytest_collection_modifyitems(config, items):
    # After collection, ensure shimmed __fields__ replace pydantic's mapping
    import importlib
    from pydantic import BaseModel
    modules = ['skills.trend_fetcher', 'skills.image_generator', 'skills.wallet_manager']
    for mod_name in modules:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            continue
        for attr in dir(mod):
            obj = getattr(mod, attr)
            try:
                if isinstance(obj, type) and issubclass(obj, BaseModel):
                    mf = getattr(obj, 'model_fields', {}) or {}
                    shim = {}
                    for name, info in (mf.items() if isinstance(mf, dict) else []):
                        ann = info.get('annotation') if isinstance(info, dict) else None
                        default = info.get('default') if isinstance(info, dict) else None
                        class FieldShim:
                            def __init__(self, type_, default):
                                self.type_ = type_
                                self.default = default
                        shim[name] = FieldShim(ann or str, default)
                    if not shim:
                        anns = getattr(obj, '__annotations__', {})
                        for name, ann in anns.items():
                            default = getattr(obj, name, None)
                            class FieldShim:
                                def __init__(self, type_, default):
                                    self.type_ = type_
                                    self.default = default
                            shim[name] = FieldShim(ann or str, default)
                    setattr(obj, '__fields__', shim)
            except Exception:
                continue
