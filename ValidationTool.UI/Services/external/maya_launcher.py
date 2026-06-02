from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MAYAPY = r"C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe"
SCRIPT = PROJECT_ROOT / "ValidationTool.UI" / "Services" / "python" / "maya_launcher.py"


def run_maya_validation():
    cmd = [ MAYAPY, str(SCRIPT) ]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)

    print(proc.stdout)

    # IMPORTANT: you should return run_id via stdout or file
    return proc.stdout