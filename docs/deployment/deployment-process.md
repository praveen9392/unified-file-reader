# Deployment & Release Runbook

Step-by-step checklist for publishing a new release to PyPI.

---

## 1. Version Bump
Make sure the version is incremented consistently across all four locations:
- `pyproject.toml` (`version = "X.Y.Z"`)
- `setup.py` (`version = "X.Y.Z"`)
- `unified_file_reader/__init__.py` (`__version__ = "X.Y.Z"`)
- `CHANGELOG.md` (Add new version section with release date and notes)

---

## 2. Pre-Release Verification
Activate your virtual environment and run all checks to ensure everything is green:

```bash
# In your virtual environment (.venv)
pytest --cov=unified_file_reader
black --check unified_file_reader tests
flake8 unified_file_reader tests
mypy unified_file_reader
isort --check unified_file_reader tests
```

---

## 3. Clean and Build Artifacts
Remove any old build files and compile the fresh distribution:

```powershell
# Clean old artifacts
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build wheel and sdist
python -m build
```

---

## 4. Validate with Twine
Check that the wheel and source tarball pass PyPI's metadata checks:

```bash
twine check dist/*
```

Both files should show `PASSED`.

---

## 5. Upload to PyPI
Upload the artifacts to PyPI:

```bash
twine upload dist/*
```
- **Username**: `__token__`
- **Password**: Your PyPI API Token (starts with `pypi-...`)

---

## 6. Git Tag & Push
Commit the version bump and create an annotated git tag:

```bash
git add pyproject.toml setup.py unified_file_reader/__init__.py CHANGELOG.md
git commit -m "chore(release): bump version to X.Y.Z"
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin master --tags
```

---

## 7. Verify Live Installation
In a fresh shell or virtual environment, verify the new release:
```bash
pip install --upgrade unified-file-reader
python -c "import unified_file_reader; print(unified_file_reader.__version__)"
```
