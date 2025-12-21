#!/usr/bin/env python3
"""
Environment information capture for benchmark reproducibility.

Captures:
- OS, kernel, CPU, memory
- Python version and implementation
- Installed packages (pip freeze)
- Git commit hash
- Timestamp
"""

import json
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_cpu_info():
    """Get CPU information."""
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                check=True,
            )
            cpu_model = result.stdout.strip()
            result = subprocess.run(
                ["sysctl", "-n", "hw.ncpu"], capture_output=True, text=True, check=True
            )
            cpu_count = result.stdout.strip()
            return f"{cpu_model} ({cpu_count} cores)"
        elif platform.system() == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        return "Unknown CPU"
    except Exception:
        return "Unknown CPU"


def get_git_commit():
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return "Not in git repo"


def get_pip_freeze():
    """Get pip freeze output."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n")
    except Exception:
        return []


def collect_env_info():
    """Collect all environment information."""
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "os": f"{platform.system()} {platform.release()}",
        "kernel": platform.version(),
        "cpu": get_cpu_info(),
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler(),
        },
        "git_commit": get_git_commit(),
        "packages": get_pip_freeze(),
    }


def main():
    """Main entry point."""
    info = collect_env_info()

    # Print human-readable format
    print("=" * 70)
    print("BENCHMARK ENVIRONMENT INFORMATION")
    print("=" * 70)
    print(f"Timestamp:    {info['timestamp']}")
    print(f"OS:           {info['os']}")
    print(f"Kernel:       {info['kernel']}")
    print(f"CPU:          {info['cpu']}")
    print(f"Python:       {info['python']['version']} ({info['python']['implementation']})")
    print(f"Git Commit:   {info['git_commit']}")
    print(f"\nInstalled Packages ({len(info['packages'])} total):")
    for pkg in info['packages']:
        if any(key in pkg.lower() for key in ['lulzprime', 'pyperf', 'primesieve', 'sympy']):
            print(f"  {pkg}")
    print("=" * 70)

    # Also save JSON for programmatic access
    output_file = Path("env_info.json")
    with open(output_file, "w") as f:
        json.dump(info, f, indent=2)
    print(f"\nJSON saved to: {output_file}")


if __name__ == "__main__":
    main()
