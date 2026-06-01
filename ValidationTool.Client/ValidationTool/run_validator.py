from misc_tools.maya_adapter import extract_meshes_from_scene

from config.validation_config import ValidationConfig

from core.runner import run_pipeline


def main():

    config = ValidationConfig(
        strict_mode=True,
        fail_on_first_error=False,
        auto_fix_enabled=False,
        include_info=True,
        include_warnings=True,
        debug_mode=False
    )

    meshes = extract_meshes_from_scene()
    run_pipeline(meshes, config)


if __name__ == "__main__":
    main()