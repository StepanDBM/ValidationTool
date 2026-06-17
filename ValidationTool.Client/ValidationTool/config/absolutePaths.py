from pathlib import Path
import sys


APP_NAME = "ValidationTool"


# ============================================================
# ENVIRONMENT DETECTION
# ============================================================

def _is_frozen() -> bool:
    """
    Returns True if running from a packaged executable.
    Works for PyInstaller / bundled Python apps.
    """
    return getattr(sys, "frozen", False)


def _find_dev_root() -> Path | None:
    """
    Walk upward from this file until we find the repository root marker.
    Returns None if not found.
    """
    p = Path(__file__).resolve()

    for parent in p.parents:
        if (parent / ".validation_root").exists():
            return parent

    return None


def _get_runtime_root() -> Path:
    """
    Root folder for tools when running in deployed/runtime mode.
    Assumes the executable/tool folder is the root.
    """
    return Path(sys.executable).resolve().parent if _is_frozen() else Path.cwd()


def get_tools_root() -> Path:
    """
    Returns the root folder where tool scripts / batch files live.

    Priority:
    1. If in dev and .validation_root exists -> use repo root
    2. Otherwise -> use runtime/exe directory
    """
    dev_root = _find_dev_root()
    if dev_root is not None:
        return dev_root

    return _get_runtime_root()


# ============================================================
# DATA ROOT (ALWAYS IN DOCUMENTS)
# ============================================================

def get_documents_root() -> Path:
    """
    Base user data folder:
        Documents/ValidationTool
    """
    return Path.home() / "Documents" / APP_NAME


TOOLS_ROOT = get_tools_root()
DATA_ROOT = get_documents_root()

# Ensure data structure exists
DATA_ROOT.mkdir(parents=True, exist_ok=True)


# ============================================================
# TOOL PATHS
# ============================================================

CLIENT_PATH = TOOLS_ROOT / "ValidationTool.Client"
UI_PATH = TOOLS_ROOT / "ValidationTool.UI"
SCENESGEN_PATH = TOOLS_ROOT / "ValidationTool.ScenesGen"

CONFIG_DIR = CLIENT_PATH / "config"
HEADLESS_DIR = CLIENT_PATH / "ValidationTool" / "misc_tools" / "headless"


# ============================================================
# DATA PATHS
# ============================================================

ARTISTS_DIR = DATA_ROOT / "Artists"
REPORTS_DIR = DATA_ROOT / "Reports"
LOGS_DIR = DATA_ROOT / "Logs"

