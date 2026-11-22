# Development & Git Workflow

Follow these guidelines when contributing code or updating documentation.

---

## 1. Branch Naming
Always branch off the latest `master` using descriptive prefixes:
- **Features**: `feature/add-yaml-reader`
- **Bug Fixes**: `fix/latin1-csv-decoding`
- **Maintenance / Dependencies**: `maintenance/bump-pypdf`
- **Documentation**: `docs/update-api-examples`

```bash
git checkout master
git pull origin master
git checkout -b feature/my-new-feature
```

---

## 2. Code Quality Standards
Before opening a Pull Request, make sure your code follows these standards:

1. **Keep Changes Focused**: Avoid mixing refactoring, feature work, and formatting changes in the same PR.
2. **Type Hints**: Add type annotations to any new functions or methods.
3. **Tests**: Add unit tests in `tests/` covering both happy paths and edge cases (e.g. empty files, bad encodings).
4. **No Leftovers**: Remove leftover print statements, debugger breakpoints, or unused imports.

---

## 3. Pre-Commit Checklist
Run the verification suite locally:

```bash
# 1. Format code
black unified_file_reader tests
isort unified_file_reader tests

# 2. Check for lint errors
flake8 unified_file_reader tests

# 3. Check types
mypy unified_file_reader

# 4. Run tests and check coverage
pytest --cov=unified_file_reader
```

---

## 4. Opening a Pull Request
1. Push your branch to GitHub:
   ```bash
   git push -u origin feature/my-new-feature
   ```
2. Open a Pull Request on GitHub.
3. Fill out the sections in the PR template (`.github/PULL_REQUEST_TEMPLATE.md`):
   - What changed
   - Why the change was made
   - Quality checklist confirmation
