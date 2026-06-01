import importlib as iL
import sys

import my_ui_module.launch_UI as lUI

def destroy_ui():
    """
    Kills any existing UI instance safely.
    Prevents ghost windows + stale Qt objects.
    """

    try:
        lUI.close_existing()
    except Exception as e:
        print("[BOOTSTRAP] UI close skipped:", e)

MODULES_TO_CLEAR = [
    "core.validation_system",
    "core",
    "checks.check_mesh",
    "config.mesh_budgets",
]

MODULES = [
    "my_ui_module.validator_UI",
    "my_ui_module.launch_UI",

    "run_validator",

    "core.validation_system",
    "core.runner",
    "core.registry",

    "config.mesh_budgets",
    "config.validation_config",
    "config.check_categories",
    "config.validation_profile",

    "checks.check_mesh",
    "checks.check_naming",
    "checks.check_uv",
    "checks.check_transforms",

    "misc_tools.maya_adapter"

    "reporting.json_reporter"
    "reporting.staged_json_reporter"
]


def reload_all():
    """
    Hard reload all pipeline modules in cor rect order.
    """

    for m in MODULES_TO_CLEAR:
        sys.modules.pop(m, None)
    for mod_name in MODULES:
        if mod_name in sys.modules:
            try:
                iL.reload(sys.modules[mod_name])
                print(f"[BOOTSTRAP] reloaded {mod_name}")
            except Exception as e:
                print(f"[BOOTSTRAP] failed reload {mod_name}: {e}")

def launch_ui():
    """
    Always creates a fresh UI instance.
    """
    return lUI.show()

def letsDoThis():
    destroy_ui()
    reload_all()
    launch_ui()