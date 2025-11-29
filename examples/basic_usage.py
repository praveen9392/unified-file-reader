"""
Basic usage examples for unified-file-reader.

This file demonstrates how to use the library for reading different file formats.
"""

from unified_file_reader import read_file
from unified_file_reader.exceptions import UnsupportedFormatError, ReaderError


def example_read_csv():
    """Example: Reading a CSV file."""
    print("=" * 50)
    print("Example 1: Reading CSV File")
    print("=" * 50)

    try:
        data = read_file("data.csv")
        print(f"Read {len(data)} rows from CSV")
        for row in data[:3]:  # Print first 3 rows
            print(row)
    except FileNotFoundError:
        print("CSV file not found. Create a sample CSV first.")


def example_read_json():
    """Example: Reading a JSON file."""
    print("\n" + "=" * 50)
    print("Example 2: Reading JSON File")
    print("=" * 50)

    try:
        config = read_file("config.json")
        print("Configuration loaded:")
        print(config)
    except FileNotFoundError:
        print("JSON file not found. Create a sample JSON first.")


def example_read_text():
    """Example: Reading a text file."""
    print("\n" + "=" * 50)
    print("Example 3: Reading Text File")
    print("=" * 50)

    try:
        content = read_file("document.txt")
        print("Text content:")
        print(content[:200])  # Print first 200 characters
    except FileNotFoundError:
        print("Text file not found. Create a sample TXT first.")


def example_read_excel():
    """Example: Reading an Excel file."""
    print("\n" + "=" * 50)
    print("Example 4: Reading Excel File")
    print("=" * 50)

    try:
        data = read_file("spreadsheet.xlsx")
        print(f"Read {len(data)} rows from Excel")
        for row in data[:3]:  # Print first 3 rows
            print(row)
    except FileNotFoundError:
        print("Excel file not found. Create a sample XLSX first.")


def example_read_pdf():
    """Example: Reading a PDF file."""
    print("\n" + "=" * 50)
    print("Example 5: Reading PDF File")
    print("=" * 50)

    try:
        text = read_file("document.pdf")
        print("PDF text content:")
        print(text[:200])  # Print first 200 characters
    except FileNotFoundError:
        print("PDF file not found. Create a sample PDF first.")


def example_read_docx():
    """Example: Reading a DOCX file."""
    print("\n" + "=" * 50)
    print("Example 6: Reading DOCX File")
    print("=" * 50)

    try:
        text = read_file("document.docx")
        print("DOCX text content:")
        print(text[:200])  # Print first 200 characters
    except FileNotFoundError:
        print("DOCX file not found. Create a sample DOCX first.")


def example_error_handling():
    """Example: Error handling."""
    print("\n" + "=" * 50)
    print("Example 7: Error Handling")
    print("=" * 50)

    # Try to read unsupported format
    try:
        data = read_file("file.xyz")
    except UnsupportedFormatError as e:
        print(f"✓ Caught UnsupportedFormatError: {e}")

    # Try to read non-existent file
    try:
        data = read_file("/nonexistent/file.csv")
    except FileNotFoundError as e:
        print(f"✓ Caught FileNotFoundError: {e}")

    # Generic error handling
    try:
        data = read_file("file.xyz")
    except ReaderError as e:
        print(f"✓ Caught ReaderError: {e}")


def example_batch_processing():
    """Example: Processing multiple files."""
    print("\n" + "=" * 50)
    print("Example 8: Batch Processing")
    print("=" * 50)

    files = [
        ("data1.csv", "CSV"),
        ("data2.json", "JSON"),
        ("document.txt", "Text"),
    ]

    for file_path, file_type in files:
        try:
            data = read_file(file_path)
            print(f"✓ Successfully read {file_type} file: {file_path}")
        except FileNotFoundError:
            print(f"✗ File not found: {file_path}")
        except UnsupportedFormatError as e:
            print(f"✗ Unsupported format: {e}")
        except ReaderError as e:
            print(f"✗ Error reading file: {e}")


def example_data_processing():
    """Example: Processing data after reading."""
    print("\n" + "=" * 50)
    print("Example 9: Data Processing")
    print("=" * 50)

    try:
        # Read CSV data
        data = read_file("employees.csv")

        # Process data
        print(f"Total employees: {len(data)}")

        # Filter data
        senior_employees = [
            emp for emp in data if int(emp.get("age", 0)) > 30
        ]
        print(f"Senior employees (age > 30): {len(senior_employees)}")

        # Group by department
        departments = {}
        for emp in data:
            dept = emp.get("department", "Unknown")
            if dept not in departments:
                departments[dept] = []
            departments[dept].append(emp)

        print(f"Departments: {list(departments.keys())}")

    except FileNotFoundError:
        print("Employee data file not found.")


def example_format_detection():
    """Example: Automatic format detection."""
    print("\n" + "=" * 50)
    print("Example 10: Automatic Format Detection")
    print("=" * 50)

    files = [
        "data.csv",
        "config.json",
        "document.txt",
        "report.xlsx",
        "manual.pdf",
        "letter.docx",
    ]

    print("Supported formats:")
    for file in files:
        ext = file.split(".")[-1]
        try:
            # This would work if files existed
            print(f"  ✓ .{ext} - Would be read automatically")
        except Exception:
            pass


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 48 + "║")
    print("║" + "  Unified File Reader - Usage Examples".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("╚" + "=" * 48 + "╝")

    # Run examples
    example_read_csv()
    example_read_json()
    example_read_text()
    example_read_excel()
    example_read_pdf()
    example_read_docx()
    example_error_handling()
    example_batch_processing()
    example_data_processing()
    example_format_detection()

    print("\n" + "=" * 50)
    print("Examples completed!")
    print("=" * 50 + "\n")
