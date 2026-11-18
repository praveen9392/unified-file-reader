# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2026-11-18

### Changed
- Upgraded core dependencies in `requirements.txt`:
  - `pypdf`: upgraded from `6.4.0` to `7.1.1` (latest stable).
  - `pandas`: upgraded from `2.3.3` to `3.1.1`.
  - `reportlab`: upgraded from `4.4.5` to `5.1.0`.
  - Modernized dev & QA tools (`pytest` 9.2.0, `black` 26.10.1, `flake8` 7.5.0, `mypy` 2.4.1, `isort` 9.0.2).
- Bumped package version to `0.1.3`.

---

## [0.1.2] - 2026-11-18

### Added
- Optional `reportlab>=3.6.0` dependency under `dev` extra for seamless local and CI PDF test execution.
- `.flake8` configuration aligning maximum line length (100) with Black and isort.
- PR raise template in `.github/PULL_REQUEST_TEMPLATE.md`.
- Comprehensive `CHANGELOG.md` tracking release milestones.

### Changed
- Standardized static type annotations (`builtins.any` -> `typing.Any`) in `supported_formats.py`.
- Enforced clean list return types in `ExcelReader` under `mypy --warn-return-any`.
- Configured `ignore_missing_imports = true` for third-party libraries under `pyproject.toml`.
- Reorganized module imports across test suites using `isort`.
- Updated contributor workflows in `CONTRIBUTING.md` and `DEVELOPMENT.md` to reference `.venv` and complete lint/coverage verification commands.

### Fixed
- Unused import warnings in `tests/conftest.py` and `unified_file_reader/utils/file_utils.py`.
- Skipping behavior in PDF test suite: all 93 tests now pass with 0 skips and 0 errors.

---

## [0.1.1] - 2026-11-18

### Changed
- Updated package version to 0.1.1 on PyPI.
- Enhanced Python 3.12 compatibility and packaging metadata.

---

## [0.1.0] - 2026-11-18

### Added
- Initial release of `unified-file-reader`.
- Unified `read_file()` API for CSV, JSON, TXT, XLSX, PDF, and DOCX formats.
- Clean Architecture with reader registry and pluggable base interfaces.
- Test suite with high coverage and comprehensive documentation.
