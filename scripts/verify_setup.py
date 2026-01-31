#!/usr/bin/env python3
"""
LexConductor - Setup Verification Script
IBM Dev Day AI Demystified Hackathon 2026

This script verifies that all required services and dependencies are properly configured.
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'=' * 80}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{BLUE}ℹ {text}{RESET}")


def check_python_version() -> bool:
    """Check if Python version is 3.11+."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print_error(
            f"Python {version.major}.{version.minor}.{version.micro} detected (3.11+ required)"
        )
        return False


def check_env_file() -> Tuple[bool, List[str]]:
    """Check if .env file exists and has required variables."""
    env_path = Path(".env")

    if not env_path.exists():
        print_error(".env file not found")
        print_info("Run: cp .env.example .env")
        return False, []

    print_success(".env file exists")

    # Required environment variables
    required_vars = [
        "WO_INSTANCE",
        "WO_API_KEY",
        "WATSONX_API_KEY",
        "WATSONX_PROJECT_ID",
        "CLOUDANT_URL",
        "CLOUDANT_API_KEY",
        "COS_ENDPOINT",
        "COS_API_KEY",
        "COS_INSTANCE_ID",
    ]

    missing_vars = []
    placeholder_vars = []

    # Load .env file
    env_vars = {}
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()

    # Check each required variable
    for var in required_vars:
        if var not in env_vars:
            missing_vars.append(var)
        elif "your_" in env_vars[var] or "your-" in env_vars[var]:
            placeholder_vars.append(var)

    if missing_vars:
        print_error(f"Missing environment variables: {', '.join(missing_vars)}")

    if placeholder_vars:
        print_warning(f"Placeholder values detected: {', '.join(placeholder_vars)}")
        print_info("Update these with your actual IBM Cloud credentials")

    if not missing_vars and not placeholder_vars:
        print_success("All required environment variables are configured")
        return True, []

    return len(missing_vars) == 0, placeholder_vars


def check_dependencies() -> bool:
    """Check if required Python packages are installed."""
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("ibm_watsonx_ai", "ibm_watsonx_ai"),
        ("ibm_watsonx_orchestrate", "ibm_watsonx_orchestrate"),
        ("ibmcloudant", "ibmcloudant"),
        ("ibm_cos_sdk", "ibm_boto3"),  # COS SDK uses boto3
        ("httpx", "httpx"),
        ("PyPDF2", "PyPDF2"),
        ("pdfplumber", "pdfplumber"),
        ("python-docx", "docx"),
        ("pytest", "pytest"),
        ("hypothesis", "hypothesis"),
    ]

    missing_packages = []

    for display_name, import_name in required_packages:
        try:
            __import__(import_name.replace("-", "_"))
            print_success(f"{display_name} installed")
        except ImportError:
            missing_packages.append(display_name)
            print_error(f"{display_name} not installed")

    if missing_packages:
        print_error(f"Missing packages: {', '.join(missing_packages)}")
        print_info("Run: pip install -r requirements.txt")
        return False

    return True


def check_orchestrate_adk() -> bool:
    """Check if watsonx Orchestrate ADK is installed."""
    import subprocess

    try:
        result = subprocess.run(
            ["orchestrate", "--version"], capture_output=True, text=True, check=True
        )

        # Extract version from output
        for line in result.stdout.split("\n"):
            if "ADK Version:" in line:
                version = line.split(":")[-1].strip()
                print_success(f"watsonx Orchestrate ADK {version} installed")
                return True

        print_success("watsonx Orchestrate ADK installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("watsonx Orchestrate ADK not found")
        print_info("Run: pip install ibm-watsonx-orchestrate")
        return False


def check_directory_structure() -> bool:
    """Check if required directories exist."""
    required_dirs = [
        "backend",
        "orchestrate",
        "orchestrate/agents",
        "docs",
        "tests",
    ]

    missing_dirs = []

    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print_success(f"{dir_path}/ exists")
        else:
            missing_dirs.append(dir_path)
            print_warning(f"{dir_path}/ not found (will be created during implementation)")

    return True  # Not critical for initial setup


def check_gitignore() -> bool:
    """Check if .gitignore properly excludes sensitive files."""
    gitignore_path = Path(".gitignore")

    if not gitignore_path.exists():
        print_error(".gitignore not found")
        return False

    with open(gitignore_path, "r") as f:
        content = f.read()

    required_patterns = [".env", "*.key", "credentials.json", "__pycache__"]

    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in content:
            missing_patterns.append(pattern)

    if missing_patterns:
        print_warning(f"Missing .gitignore patterns: {', '.join(missing_patterns)}")
    else:
        print_success(".gitignore properly configured")

    return len(missing_patterns) == 0


def print_next_steps(has_placeholders: bool):
    """Print next steps for the user."""
    print_header("NEXT STEPS")

    if has_placeholders:
        print_info("1. Configure IBM Cloud Services:")
        print("   - Create Cloudant instance (Lite plan, US-South)")
        print("   - Create Cloud Object Storage instance (Lite plan, US-South)")
        print("   - Create Code Engine project (Osaka region)")
        print("   - Get watsonx Orchestrate credentials")
        print("   - Get watsonx.ai credentials")
        print()
        print_info("2. Update .env file with your credentials")
        print()

    print_info("3. Verify connectivity:")
    print("   python scripts/test_connections.py")
    print()
    print_info("4. Start development:")
    print("   - Implement data models (backend/models.py)")
    print("   - Create agent implementations (backend/agents/)")
    print("   - Deploy to Code Engine")
    print()
    print_info("5. Hackathon Deadline: February 1, 2026 - 10:00 AM ET")


def main():
    """Main verification function."""
    print_header("LexConductor - Setup Verification")
    print_info("IBM Dev Day AI Demystified Hackathon 2026")
    print_info("Team: AI Kings 👑")

    checks = []

    # Run all checks
    print_header("Checking Python Environment")
    checks.append(("Python Version", check_python_version()))

    print_header("Checking Dependencies")
    checks.append(("Python Packages", check_dependencies()))
    checks.append(("watsonx Orchestrate ADK", check_orchestrate_adk()))

    print_header("Checking Configuration")
    env_ok, placeholders = check_env_file()
    checks.append(("Environment Variables", env_ok))
    checks.append((".gitignore", check_gitignore()))

    print_header("Checking Project Structure")
    checks.append(("Directory Structure", check_directory_structure()))

    # Summary
    print_header("VERIFICATION SUMMARY")

    passed = sum(1 for _, result in checks if result)
    total = len(checks)

    for name, result in checks:
        if result:
            print_success(f"{name}: PASS")
        else:
            print_error(f"{name}: FAIL")

    print()
    if passed == total:
        print_success(f"All checks passed ({passed}/{total})")
        if placeholders:
            print_warning("Some environment variables have placeholder values")
            print_warning("Update .env with your actual IBM Cloud credentials")
    else:
        print_error(f"Some checks failed ({passed}/{total} passed)")

    # Print next steps
    print_next_steps(len(placeholders) > 0)

    return passed == total and len(placeholders) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
