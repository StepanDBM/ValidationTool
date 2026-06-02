from pathlib import Path
import sys

p = Path(__file__).resolve()

# Walk upward until we find the project root
for parent in p.parents:
    if (parent / "misc_tools").exists():
        PROJECTROOT = parent
        break
else:
    raise RuntimeError("Could not locate project root")

sys.path.insert(0, str(PROJECTROOT))

from misc_tools.headless.maya_sceneBuilder import build_test_scene
from misc_tools.headless.maya_session import run_headless_pipeline


def main():
    build_test_scene()

    result = run_headless_pipeline()

    print("\nDONE")
    print("Run ID:", result.run_id)
    print("Assets:", len(result.assets))


if __name__ == "__main__":
    main()