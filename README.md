# CLI Standard Kit (Python Installer Version)

This package provides a **self-installing CLI** for creating standardized Python command-line tools.

## 🚀 Usage

```bash
pip install git+https://github.com/c3nk/cookiecutter-cli-standard-kit.git
cli-standard-kit init mytool
```

### What it does
1. Generates a new project from the cookiecutter template  
2. Initializes a local Git repository  
3. Creates and activates a `.venv` environment  
4. Provides ready-to-run CLI structure following standard rules

### Example output
```
🚀 Creating new CLI project: mytool
📁 Entered: /path/to/mytool
🐍 Creating virtual environment (.venv)...
✅ Virtual environment created.
📦 Project ready!
➡ cd mytool && source .venv/bin/activate && python src/mytool/cli.py --help
```
