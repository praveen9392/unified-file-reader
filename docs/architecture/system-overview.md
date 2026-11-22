# System Architecture

Unified File Reader is structured to keep each file format completely isolated from the others. Instead of one massive script filled with `if extension == ".csv"` checks, the codebase follows Clean Architecture and standard SOLID design patterns.

```
                    +-----------------------------+
                    |        Your Application     |
                    +-----------------------------+
                                   |
                                   v  read_file("data.xlsx")
                    +-----------------------------+
                    |          api.py             |
                    | (Validation & Orchestration)|
                    +-----------------------------+
                                   |
                                   v  get_reader_for_extension(".xlsx")
                    +-----------------------------+
                    |         registry.py         |
                    |   (In-Memory Dispatcher)    |
                    +-----------------------------+
                                   |
                                   v  BaseReader contract
             +---------------------+---------------------+
             |                     |                     |
             v                     v                     v
      +--------------+      +--------------+      +--------------+
      |  CSVReader   |      | ExcelReader  |      |  PDFReader   |
      +--------------+      +--------------+      +--------------+
```

---

## Codebase Layers

### 1. Public API (`unified_file_reader/api.py`)
This is the only module most users interact with. It exposes `read_file(path)` and acts as a coordinator:
1. Validates that the file exists and isn't a directory.
2. Extracts the file extension.
3. Asks the registry for a reader that can handle that extension.
4. Calls `reader.read(path)` and hands the parsed data back to the caller.

### 2. The Registry (`unified_file_reader/registry.py`)
The registry manages an internal dictionary mapping extensions to reader instances. When the package is imported, all built-in readers automatically register themselves. 

It also gives developers a public `register_reader()` function to plug in custom file parsers at runtime.

### 3. Base Reader Contract (`unified_file_reader/interfaces/base_reader.py`)
An abstract base class (`BaseReader`) that every reader must inherit from:
- `supported_extensions`: List of file extensions the reader handles (e.g. `[".csv"]`).
- `can_read(extension)`: Returns `True` if the reader supports that format.
- `read(path)`: The method that actually opens, parses, and returns the file contents.

### 4. Concrete Readers (`unified_file_reader/readers/`)
Each file format has its own isolated file:
- `csv_reader.py`
- `json_reader.py`
- `txt_reader.py`
- `excel_reader.py`
- `pdf_reader.py`
- `docx_reader.py`

If you ever need to optimize Excel reading or fix a bug in Word document parsing, you only ever need to work within that specific reader module.

### 5. Utility Layer (`unified_file_reader/utils/file_utils.py`)
Small, focused functions used across readers and the API layer: checking file existence, verifying read permissions, and extracting extensions safely.
