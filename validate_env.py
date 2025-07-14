# validate_env.py

import os
import sys
import subprocess

REQUIRED_ENV_VARS = ["HF_TOKEN", "WOLFRAM_APP_ID"]
REQUIRED_PACKAGES = ["Flask", "torch", "transformers"]

def check_env_file():
    if not os.path.isfile(".env"):
        print("❌ .env file is missing. Please create one using .env.example.")
        return False
    print("✅ .env file found.")
    return True

def check_env_keys():
    missing = []
    with open(".env") as f:
        env_content = f.read()
        for key in REQUIRED_ENV_VARS:
            if key not in env_content:
                missing.append(key)
    if missing:
        print(f"❌ Missing env keys: {', '.join(missing)}")
        return False
    print("✅ Required keys present in .env")
    return True

def check_python_packages():
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"❌ Missing Python packages: {', '.join(missing)}")
        print("ℹ️ Run: pip install -r requirements.txt")
        return False
    print("✅ Required Python packages are installed.")
    return True

def check_flask_boot():
    try:
        subprocess.run(["python", "main.py"], timeout=5)
        print("✅ Flask app launched successfully.")
        return True
    except Exception as e:
        print(f"❌ Flask launch failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Running Mythiq post-clone validator...\n")
    all_good = (
        check_env_file() and
        check_env_keys() and
        check_python_packages()
    )
    if all_good:
        print("\n✅ Environment looks good! You're ready to launch Mythiq.")
    else:
        print("\n❌ Environment setup incomplete. Fix above issues before continuing.")
