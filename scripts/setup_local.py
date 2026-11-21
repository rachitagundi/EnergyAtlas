"""Install the catalogue dependencies in the project, without models or API keys."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import venv

from check_setup import check_fullstack_files


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    if sys.version_info[:2] != (3, 12):
        print("This checkpoint is pinned for Python 3.12. Run python --version and use a Python 3.12 installation.")
        return 1
    missing = check_fullstack_files(root)["missing_files"]
    if missing:
        print("The extracted project is incomplete. Re-extract the integrated ZIP into a new folder.")
        print("Missing: " + ", ".join(missing))
        return 1
    node = shutil.which("node")
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm")
    if not node or not npm:
        print("Node.js and npm are required. This checkpoint was built with Node 24.")
        return 1
    major = int(subprocess.check_output([node, "--version"], text=True).strip().lstrip("v").split(".")[0])
    if major < 24:
        print("Use Node 24 for this checkpoint; current Node is older.")
        return 1
    environment = root / ".venv-fullstack"
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        print("Creating the isolated backend environment…", flush=True)
        venv.create(environment, with_pip=True)
    commands = [
        [str(python), "-m", "pip", "install", "-r", "backend/requirements.txt", "-c", "backend/constraints-py312.txt"],
        [str(python), "-m", "pip", "check"],
        ([os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", npm, "--prefix", "frontend", "ci"] if os.name == "nt" else [npm, "--prefix", "frontend", "ci"]),
    ]
    for command in commands:
        result = subprocess.run(command, cwd=root, check=False)
        if result.returncode:
            print("Setup stopped at the failed command. Keep its error output for troubleshooting.")
            return result.returncode
    print("\nSetup complete. In this project folder, run npm.cmd run dev on Windows or npm run dev on Linux.")
    print("Then open http://127.0.0.1:5173")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
