import subprocess, sys, os
from pathlib import Path

def run(cmd, **kwargs):
    print(f"▶ {cmd}")
    subprocess.run(cmd, shell=True, check=True, **kwargs)

def run_init():
    if len(sys.argv) < 2:
        print("❌ Usage: cli-standard-kit init <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    print(f"🚀 Creating new CLI project: {project_name}")

    # Cookiecutter ile proje oluştur
    run(f"cookiecutter gh:c3nk/cookiecutter-cli-standard-kit --no-input "
        f"project_name='{project_name}' project_slug='{project_name}'")

    os.chdir(project_name)
    print("📁 Entered:", os.getcwd())

    # Git başlat
    run("git init -q && git add . && git commit -m 'init project'")
    run("git branch -M main")

    # venv oluştur
    print("🐍 Creating virtual environment (.venv)...")
    run("python3 -m venv .venv")
    print("✅ Virtual environment created.")

    print("\n📦 Project ready!")
    print(f"➡ cd {project_name} && source .venv/bin/activate && python src/{project_name}/cli.py --help")
