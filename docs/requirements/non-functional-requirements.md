# Non-Functional Requirements

## 1. Type Safety & Editor Support
- **Full Type Hints**: Every public function and internal helper includes explicit PEP 484 type hints.
- **Mypy Validation**: The package passes `mypy unified_file_reader` with `--warn-return-any` enabled.
- **`py.typed` Included**: Ships with the PEP 561 marker so consumer IDEs (VS Code, PyCharm, Neovim) get instant auto-completion and static analysis out of the box.

---

## 2. Testing & Quality Standards
- **100% Pass Rate**: Every release requires all tests to pass (93 passed, 0 skipped, 0 failed).
- **No Skips in CI**: Dependencies like `reportlab` are pinned in `dev` extras so that tests requiring PDF fixtures execute everywhere without being skipped.
- **Code Coverage**: The core codebase maintains over 90% test coverage across readers, registry, and utility logic.
- **Style Consistency**:
  - `black`: Formatted to 100 character line length.
  - `isort`: Standard library, third-party, and first-party imports grouped cleanly.
  - `flake8`: Configured with matching 100 character line limit in `.flake8`.

---

## 3. Python Compatibility & Environments
- **Recommended Python**: Developed and actively tested on **Python 3.12** (specifically 3.12.8).
- **Compatibility Window**: Compatible with Python 3.9 through 3.12.
- **Cross-Platform**: Operates consistently across Windows, macOS, and Linux without platform-specific code.

---

## 4. Architecture & Maintainability
- **Single Responsibility**: Each reader lives in its own module inside `unified_file_reader/readers/`. If a bug appears in PDF parsing, you only touch `pdf_reader.py`.
- **Open for Extension**: Adding new file types does not require editing existing readers or the core `read_file()` dispatcher.
- **Loose Coupling**: The top-level `read_file()` entry point depends on the abstract `BaseReader` interface rather than hardcoded reader instances.
