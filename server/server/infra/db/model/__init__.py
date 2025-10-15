import importlib
import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder using the current package name as prefix."""
    package_dir = Path(__file__).resolve().parent
    # Use dynamic prefix so this works whether imported as 'server.infra.db.model'
    # or via another package base during test discovery.
    prefix = __name__ + "."
    for module in pkgutil.walk_packages(path=[str(package_dir)], prefix=prefix):
        importlib.import_module(module.name)  # noqa: WPS421


# Only attempt to auto-load when this package is imported normally
try:
    load_all_models()
except Exception:
    # Be resilient during tooling/test discovery; models will be loaded at runtime.
    pass
