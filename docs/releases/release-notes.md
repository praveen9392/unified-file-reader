# Release Notes

Changelog and release notes for all published versions of `unified-file-reader`.

---

## v0.1.3 (2026-11-18)
### What Changed
- **Updated Core Dependencies**:
  - `pypdf`: Upgraded from `6.4.0` to `7.1.1` for faster and more resilient PDF parsing.
  - `pandas`: Upgraded from `2.3.3` to `3.1.1`.
  - `reportlab`: Upgraded from `4.4.5` to `5.1.0`.
  - Modernized developer dependencies (`pytest` 9.2.0, `black` 26.10.1, `flake8` 7.5.0, `mypy` 2.4.1, `isort` 9.0.2).
- **Quality**: Maintained 100% test pass rate across all 93 test cases with 0 skips.

---

## v0.1.2 (2026-11-18)
### What Changed
- **Strict Typing Compliance**: Fixed type hints in `supported_formats.py` (`builtins.any` -> `typing.Any`) and added explicit list casting in `ExcelReader` to resolve `mypy --warn-return-any` warnings.
- **Test Suite Unlocked**: Added `reportlab>=3.6.0` to optional `dev` dependencies so all PDF tests execute without skips.
- **Linter Harmonization**: Added `.flake8` configuration matching Black's 100-character line length to avoid false-positive lint warnings.
- **Workflow Improvements**: Added standard GitHub Pull Request template (`.github/PULL_REQUEST_TEMPLATE.md`) and updated contributor setup documentation.

---

## v0.1.1 (2026-11-18)
### What Changed
- Updated packaging metadata for PyPI.
- Enhanced Python 3.12 compatibility settings.

---

## v0.1.0 (2026-11-18) - Initial Release
### What Changed
- Initial open-source release on PyPI.
- Core `read_file()` helper function supporting CSV, JSON, TXT, Excel (XLSX), PDF, and Word (DOCX).
- Pluggable `BaseReader` interface and `ReaderRegistry` pattern.
- Comprehensive test suite and developer documentation.
