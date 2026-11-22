# Development Setup

Quick guide to get your local environment set up for developing or contributing to `unified-file-reader`.

---

## 1. Prerequisites
- **Python**: 3.12 (developed and tested on Python 3.12.8; versions 3.9 through 3.12 work as well).
- **Git**
- **pip**

---

## 2. Clone the Repository
```bash
git clone https://github.com/praveen9392/unified-file-reader.git
cd unified-file-reader
```

---

## 3. Set Up a Virtual Environment
We recommend creating a local `.venv` so dependencies don't interfere with your global Python installation:

### On Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### On Windows (CMD)
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### On macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install Dependencies
Install the package in editable mode along with all developer tooling:

```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

*Note: If you want to mirror the exact locked dependency versions from the repository, you can alternatively run `pip install -r requirements.txt`.*

---

## 5. Verify Your Environment
Run the test suite and quality checks to confirm everything is working properly:

```bash
pytest
black --check unified_file_reader tests
flake8 unified_file_reader tests
mypy unified_file_reader
isort --check unified_file_reader tests
```

If all 93 tests pass and the linters produce no errors, you're ready to start coding!
