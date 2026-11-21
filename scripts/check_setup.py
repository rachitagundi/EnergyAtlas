"""Print read-only setup diagnostics without third-party packages or network calls."""

from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def read_command(arguments: list[str]) -> str | None:
    """Optional programs may be absent or slow; diagnostics must still complete."""
    try:
        result = subprocess.run(
            arguments, capture_output=True, text=True, timeout=15, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def check_fullstack_files(project_directory: Path) -> dict:
    required = [
        "package.json", "frontend/package.json", "frontend/package-lock.json",
        "backend/requirements.txt", "backend/constraints-py312.txt",
        "backend/app/main.py", "scripts/dev.mjs",
    ]
    missing = [name for name in required if not (project_directory / name).is_file()]
    return {"complete": not missing, "missing_files": missing}


def collect_setup() -> dict:
    system = platform.system()
    notes = []
    ram_bytes = None
    cpu = platform.processor() or platform.machine()
    gpu_names = []

    if system == "Windows":
        powershell = shutil.which("powershell") or shutil.which("pwsh")
        script = (
            "$ErrorActionPreference='Stop'; "
            "[pscustomobject]@{ "
            "ram_bytes=(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory; "
            "cpu=@(Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name); "
            "gpu_names=@(Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name) "
            "} | ConvertTo-Json -Compress"
        )
        raw = read_command([powershell, "-NoProfile", "-NonInteractive", "-Command", script]) if powershell else None
        if raw:
            try:
                details = json.loads(raw)
                ram_bytes = int(details["ram_bytes"])
                cpu = details.get("cpu", cpu)
                gpu_names = details.get("gpu_names", [])
            except (ValueError, TypeError, KeyError):
                notes.append("Windows hardware query could not be parsed.")
        else:
            notes.append("Windows hardware query unavailable; provide RAM and GPU names manually.")
    elif hasattr(os, "sysconf"):
        try:
            ram_bytes = os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE")
        except (OSError, ValueError):
            notes.append("Total RAM could not be measured.")

    project_directory = Path(__file__).resolve().parents[1]
    git_path = shutil.which("git")
    node_path = shutil.which("node")
    npm_path = shutil.which("npm.cmd" if system == "Windows" else "npm")
    notes.append("GPU names do not establish usable VRAM or model performance.")
    notes.append("No model selection, installation, download or API call was performed.")
    return {
        "schema_version": 1,
        "system": system,
        "python": {
            "version": platform.python_version(),
            "meets_minimum_3_11": sys.version_info >= (3, 11),
            "matches_tested_minor_3_12": sys.version_info[:2] == (3, 12),
        },
        "git": {
            "available": bool(git_path),
            "version": read_command([git_path, "--version"]) if git_path else None,
        },
        "node": {
            "available": bool(node_path),
            "version": read_command([node_path, "--version"]) if node_path else None,
        },
        "npm": {"available": bool(npm_path)},
        "project": {
            "directory": str(project_directory),
            "fullstack": check_fullstack_files(project_directory),
        },
        "cpu": cpu,
        "total_ram_gib": round(ram_bytes / 2**30, 1) if ram_bytes else None,
        "gpu_names": gpu_names,
        "project_disk_free_gib": round(shutil.disk_usage(project_directory).free / 2**30, 1),
        "ollama_command_available": bool(shutil.which("ollama")),
        "vscode_command_available": bool(shutil.which("code") or shutil.which("code.cmd")),
        "notes": notes,
    }


if __name__ == "__main__":
    print(json.dumps(collect_setup(), indent=2, ensure_ascii=False))
