# Configuration Reference

Here is a quick breakdown of the configuration files in the project and what they do.

---

## `pyproject.toml`
The single source of truth for package metadata, dependencies, and tool settings:

- **Build System**: Uses standard `setuptools.build_meta`.
- **Runtime Dependencies**:
  - `pandas>=1.5.0`
  - `openpyxl>=3.0.0`
  - `pypdf>=3.0.0`
  - `python-docx>=0.8.11`
- **Developer Dependencies (`[project.optional-dependencies].dev`)**:
  - `pytest>=7.0.0`, `pytest-cov>=4.0.0`
  - `black>=23.0.0`, `flake8>=6.0.0`, `isort>=5.12.0`, `mypy>=1.0.0`
  - `reportlab>=3.6.0` (used to generate dynamic PDF test fixtures on the fly)
- **Tool Settings**:
  - `[tool.black]`: Sets max line length to `100` targeting Python 3.12.
  - `[tool.isort]`: Configured with `profile = "black"` and line length `100`.
  - `[tool.mypy]`: Targets Python 3.12, enables `warn_return_any`, and sets `ignore_missing_imports = true` for third-party libraries without stubs.

---

## `.flake8`
Centralized Flake8 configuration to prevent conflicts with Black and isort:

```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude = .git, __pycache__, build, dist, .venv, venv, .pytest_cache
```

---

## `pytest.ini`
Configures the test runner:
- Enables verbose test execution (`-v`).
- Enforces strict marker checks (`--strict-markers`).
- Hides noisy external library warnings (`--disable-warnings`).
- Declares standard markers: `unit`, `integration`, and `slow`.

---

## `MANIFEST.in`
Ensures non-Python files like `README.md`, `LICENSE`, and `requirements.txt` are included when creating source distributions (`sdist`).
