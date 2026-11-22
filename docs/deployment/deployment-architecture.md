# Deployment Architecture

How the package is built, distributed, and consumed.

---

## Overview

Unified File Reader is a **pure Python package**. It doesn't compile C extensions or require platform-specific binaries, which means a single built wheel runs on Windows, macOS, and Linux without modification.

```
+-----------------------------------------------------------+
|                   Source Repository                       |
|        (GitHub: praveen9392/unified-file-reader)          |
+-----------------------------------------------------------+
                             |
                             | python -m build
                             v
+-----------------------------------------------------------+
|                     dist/ Directory                       |
|  - unified_file_reader-X.Y.Z-py3-none-any.whl (Wheel)     |
|  - unified_file_reader-X.Y.Z.tar.gz           (sdist)     |
+-----------------------------------------------------------+
                             |
                             | twine upload dist/*
                             v
+-----------------------------------------------------------+
|                        PyPI.org                           |
|       (https://pypi.org/project/unified-file-reader/)     |
+-----------------------------------------------------------+
                             |
                             | pip install unified-file-reader
                             v
+-----------------------------------------------------------+
|                   End-User Environment                    |
+-----------------------------------------------------------+
```

---

## Artifact Types

### 1. The Wheel (`.whl`)
- Filename format: `unified_file_reader-X.Y.Z-py3-none-any.whl`
- Contains pre-packaged Python files, metadata, and license.
- Installs in seconds via pip because no building or compiling is required on the user's machine.

### 2. The Source Distribution (`.tar.gz`)
- Filename format: `unified_file_reader-X.Y.Z.tar.gz`
- Contains the raw source code, test suite, `LICENSE`, `README.md`, and `requirements.txt`.
- Provides an archival fallback if a user needs to build from source or package the library for Linux distributions.
