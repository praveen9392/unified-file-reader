# Architecture Decision Records (ADRs)

Key technical choices, context, and trade-offs made while designing the library.

---

## ADR-001: Centralized Registry vs Hardcoded Switch Statements
- **Date**: 2026-11
- **Status**: Accepted
- **Context**: Different file formats require completely different libraries (`pandas`, `pypdf`, `python-docx`). Putting a big `if / elif` chain in `api.py` would mean modifying the main entry point every time someone adds a format, violating the Open/Closed Principle.
- **Decision**: Use a simple registry pattern (`ReaderRegistry`) where readers register their extensions. The API layer just asks the registry for a handler.
- **Trade-off**: Slightly more boilerplate (an abstract base class and a registration step), but in return, the codebase stays clean and users can register their own custom readers without hacking the library.

---

## ADR-002: In-Memory Results vs Streaming
- **Date**: 2026-11
- **Status**: Accepted
- **Context**: When reading small to medium files (configuration files, reports, spreadsheets), developers usually want the data right away as a standard Python `list`, `dict`, or `str` without dealing with generator boilerplate.
- **Decision**: Read the full file contents into memory and return the final data structure directly.
- **Trade-off**: Very intuitive for standard use cases. However, multi-gigabyte files will consume significant RAM. A dedicated streaming API (`read_file_stream`) is earmarked for a future minor release.

---

## ADR-003: Graceful Encoding Fallback (UTF-8 to Latin-1)
- **Date**: 2026-11
- **Status**: Accepted
- **Context**: In real-world data pipelines, CSV and text files frequently contain mixed encodings (such as Western European `latin-1` or Windows-1252) that blow up with `UnicodeDecodeError` in standard `open(..., encoding='utf-8')`.
- **Decision**: Both `CSVReader` and `TXTReader` try `utf-8` first. If decoding fails, they immediately retry with `latin-1`.
- **Trade-off**: Prevents annoying crashes on common data exports without requiring the user to manually pass encoding flags for 95% of use cases.

---

## ADR-004: Clean Architecture and PEP 484 Types
- **Date**: 2026-11
- **Status**: Accepted
- **Context**: Developers rely on autocomplete, type checks, and clear interfaces when integrating third-party libraries.
- **Decision**: Ship `py.typed`, maintain complete type annotations across all modules, and enforce `mypy` in CI.
- **Trade-off**: Requires keeping annotations up to date when modifying readers, but catches bugs early and creates a great developer experience.
