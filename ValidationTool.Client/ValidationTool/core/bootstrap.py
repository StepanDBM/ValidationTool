import sys
import importlib as iL

import my_ui_module.launch_UI as lUI


MODULES_TO_CLEAR = [
    "core",
    "core.validation_system",
    "core.runner",
    "core.registry",
    "core.validation_context",

    "config.mesh_budgets",
    "config.validation_config",
    "config.check_categories",
    "config.validation_profile",

    "checks.check_mesh",
    "checks.check_naming",
    "checks.check_uv",
    "checks.check_transforms",

    "misc_tools.maya_adapter",
    "reporting.json_reporter",
    "reporting.staged_json_reporter",

    "my_ui_module.validator_UI",
    "my_ui_module.launch_UI",
    "run_validator",
]


def destroy_ui():
    try:
        lUI.close_existing()
    except Exception as e:
        print("[BOOTSTRAP] UI close skipped:", e)


def hard_reload():
    # 1. kill modules
    for m in MODULES_TO_CLEAR:
        if m in sys.modules:
            del sys.modules[m]

    # 2. force garbage collection helps Maya a bit
    import gc
    gc.collect()

    # 3. re-import entry UI AFTER cleanup
    global lUI
    lUI = iL.import_module("my_ui_module.launch_UI")

    print("[BOOTSTRAP] reload complete")


def launch_ui():
    return lUI.show()


def letsDoThis():
    destroy_ui()
    hard_reload()
    launch_ui()