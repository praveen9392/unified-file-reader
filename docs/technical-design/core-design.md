# Core Technical Design & Extensibility

## The BaseReader Contract
Every reader in the library subclasses `BaseReader` (found in `unified_file_reader/interfaces/base_reader.py`):

```python
from abc import ABC, abstractmethod
from typing import Any, List

class BaseReader(ABC):
    """Abstract base class for all file readers."""

    supported_extensions: List[str] = []

    @abstractmethod
    def can_read(self, extension: str) -> bool:
        """Check if this reader can handle the given file extension."""
        pass

    @abstractmethod
    def read(self, path: str) -> Any:
        """Read the file and return its parsed contents."""
        pass
```

Because `BaseReader` enforces this contract, the rest of the system never needs to care whether it's reading a simple text file or extracting text from a binary PDF stream.

---

## The Registry
The registry (`unified_file_reader/registry.py`) holds an internal mapping of lowercase file extensions to reader instances:

- `register_reader(reader)`: Registers a reader instance for all extensions declared in its `supported_extensions` list.
- `get_reader_for_extension(extension)`: Looks up and returns the right reader, raising `UnsupportedFormatError` if there's no match.
- `get_supported_extensions()`: Returns a list of all currently supported extensions.

---

## How to Add a Custom Reader
Adding support for your own file format is straightforward. Here's a real example showing how to add a YAML reader using `pyyaml`:

```python
import yaml
from typing import Any
from unified_file_reader import read_file
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.registry import register_reader
from unified_file_reader.utils.file_utils import ensure_file_exists

class YAMLReader(BaseReader):
    # 1. Define supported extensions
    supported_extensions = [".yaml", ".yml"]

    # 2. Check extension support
    def can_read(self, extension: str) -> bool:
        return extension.lower() in self.supported_extensions

    # 3. Implement file parsing logic
    def read(self, path: str) -> Any:
        ensure_file_exists(path)
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

# 4. Register your reader with the system
register_reader(YAMLReader())

# 5. Now read_file works with YAML files automatically!
config = read_file("server_config.yaml")
print(config["database"]["host"])
```

This pattern makes it easy to add readers for domain-specific formats like Parquet, HDF5, XML, or shapefiles without modifying the library source code.
