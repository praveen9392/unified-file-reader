"""
Advanced usage examples for unified-file-reader.

This file demonstrates advanced features and patterns.
"""

from unified_file_reader import read_file
from unified_file_reader.registry import (
    get_reader_for_extension,
    get_all_readers,
    get_supported_extensions,
    register_reader,
)
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.exceptions import UnsupportedFormatError


def example_custom_reader():
    """Example: Creating and registering a custom reader."""
    print("=" * 50)
    print("Example 1: Custom Reader")
    print("=" * 50)

    # Define a custom reader
    class TOMLReader(BaseReader):
        """Custom reader for TOML files."""

        supported_extensions = [".toml"]

        def can_read(self, extension: str) -> bool:
            return extension.lower() in self.supported_extensions

        def read(self, path: str):
            # In real implementation, would use tomli or tomllib
            print(f"Reading TOML file: {path}")
            return {"example": "toml data"}

    # Register the custom reader
    register_reader(TOMLReader())
    print("✓ Custom TOML reader registered")

    # Now it's available
    reader = get_reader_for_extension(".toml")
    print(f"✓ Reader found for .toml: {reader.__class__.__name__}")


def example_list_supported_formats():
    """Example: List all supported formats."""
    print("\n" + "=" * 50)
    print("Example 2: List Supported Formats")
    print("=" * 50)

    extensions = get_supported_extensions()
    print(f"Supported formats ({len(extensions)}):")
    for ext in sorted(extensions):
        print(f"  • {ext}")


def example_list_all_readers():
    """Example: List all registered readers."""
    print("\n" + "=" * 50)
    print("Example 3: List All Readers")
    print("=" * 50)

    readers = get_all_readers()
    print(f"Registered readers ({len(readers)}):")
    for reader in readers:
        exts = getattr(reader, "supported_extensions", [])
        print(f"  • {reader.__class__.__name__}: {', '.join(exts)}")


def example_direct_reader_usage():
    """Example: Using readers directly."""
    print("\n" + "=" * 50)
    print("Example 4: Direct Reader Usage")
    print("=" * 50)

    # Get a specific reader
    reader = get_reader_for_extension(".json")

    if reader:
        print(f"Using reader: {reader.__class__.__name__}")
        print(f"Can read .json: {reader.can_read('.json')}")
        print(f"Can read .csv: {reader.can_read('.csv')}")

        # Use reader directly (if file exists)
        try:
            data = reader.read("config.json")
            print("✓ File read successfully")
        except FileNotFoundError:
            print("✗ File not found (expected in this example)")


def example_format_detection_by_extension():
    """Example: Detect format by file extension."""
    print("\n" + "=" * 50)
    print("Example 5: Format Detection")
    print("=" * 50)

    test_files = [
        "data.csv",
        "config.json",
        "document.txt",
        "report.xlsx",
        "manual.pdf",
        "letter.docx",
        "unknown.xyz",
    ]

    for file_path in test_files:
        ext = "." + file_path.split(".")[-1]
        reader = get_reader_for_extension(ext)

        if reader:
            print(f"✓ {file_path:20} -> {reader.__class__.__name__}")
        else:
            print(f"✗ {file_path:20} -> Not supported")


def example_error_handling_advanced():
    """Example: Advanced error handling."""
    print("\n" + "=" * 50)
    print("Example 6: Advanced Error Handling")
    print("=" * 50)

    def safe_read_file(path: str, default=None):
        """Safely read a file with fallback."""
        try:
            return read_file(path)
        except FileNotFoundError:
            print(f"  File not found: {path}")
            return default
        except UnsupportedFormatError:
            print(f"  Format not supported: {path}")
            return default
        except Exception as e:
            print(f"  Error reading file: {e}")
            return default

    # Try reading files
    print("Attempting to read files:")
    safe_read_file("data.csv", default=[])
    safe_read_file("config.json", default={})
    safe_read_file("unknown.xyz", default=None)


def example_batch_read_with_validation():
    """Example: Batch reading with validation."""
    print("\n" + "=" * 50)
    print("Example 7: Batch Read with Validation")
    print("=" * 50)

    def read_and_validate(file_path: str, expected_type: type):
        """Read file and validate result type."""
        try:
            data = read_file(file_path)
            if isinstance(data, expected_type):
                print(f"✓ {file_path}: Valid {expected_type.__name__}")
                return data
            else:
                print(
                    f"✗ {file_path}: Expected {expected_type.__name__}, "
                    f"got {type(data).__name__}"
                )
                return None
        except Exception as e:
            print(f"✗ {file_path}: {e}")
            return None

    # Validate file types
    print("Validating file types:")
    read_and_validate("data.csv", list)
    read_and_validate("config.json", dict)
    read_and_validate("document.txt", str)


def example_reader_capabilities():
    """Example: Check reader capabilities."""
    print("\n" + "=" * 50)
    print("Example 8: Reader Capabilities")
    print("=" * 50)

    readers = get_all_readers()

    print("Reader capabilities:")
    for reader in readers:
        print(f"\n{reader.__class__.__name__}:")
        exts = getattr(reader, "supported_extensions", [])
        print(f"  Extensions: {', '.join(exts)}")
        print(f"  Can read .csv: {reader.can_read('.csv')}")
        print(f"  Can read .json: {reader.can_read('.json')}")
        print(f"  Can read .txt: {reader.can_read('.txt')}")


def example_performance_consideration():
    """Example: Performance considerations."""
    print("\n" + "=" * 50)
    print("Example 9: Performance Considerations")
    print("=" * 50)

    print("Performance tips:")
    print("1. Readers are instantiated once and reused")
    print("2. Use direct reader access for repeated reads")
    print("3. Large files are handled efficiently")
    print("4. Minimal dependencies per reader")

    # Example: Reuse reader for multiple files
    print("\nReusing reader for multiple files:")
    reader = get_reader_for_extension(".csv")
    if reader:
        print(f"Using {reader.__class__.__name__}")
        files = ["data1.csv", "data2.csv", "data3.csv"]
        for file in files:
            print(f"  Would read: {file}")


def example_extensibility():
    """Example: Extensibility patterns."""
    print("\n" + "=" * 50)
    print("Example 10: Extensibility")
    print("=" * 50)

    print("The library is designed to be extended:")
    print("\n1. Add new reader:")
    print("   - Create class inheriting from BaseReader")
    print("   - Implement can_read() and read() methods")
    print("   - Register with register_reader()")

    print("\n2. Custom processing:")
    print("   - Read file with read_file()")
    print("   - Process data as needed")
    print("   - No changes to library needed")

    print("\n3. Integration:")
    print("   - Use as library in your project")
    print("   - Extend with custom readers")
    print("   - Maintain clean architecture")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 48 + "║")
    print("║" + "  Unified File Reader - Advanced Examples".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("╚" + "=" * 48 + "╝")

    # Run examples
    example_custom_reader()
    example_list_supported_formats()
    example_list_all_readers()
    example_direct_reader_usage()
    example_format_detection_by_extension()
    example_error_handling_advanced()
    example_batch_read_with_validation()
    example_reader_capabilities()
    example_performance_consideration()
    example_extensibility()

    print("\n" + "=" * 50)
    print("Advanced examples completed!")
    print("=" * 50 + "\n")
