"""
Pytest configuration and fixtures.

Provides shared test resources and utilities.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_csv_file(temp_dir):
    """Create a sample CSV file."""
    csv_path = os.path.join(temp_dir, "sample.csv")
    with open(csv_path, "w", newline="") as f:
        f.write("name,age,city\n")
        f.write("John,30,New York\n")
        f.write("Jane,28,Los Angeles\n")
        f.write("Bob,35,Chicago\n")
    return csv_path


@pytest.fixture
def sample_json_file(temp_dir):
    """Create a sample JSON file."""
    json_path = os.path.join(temp_dir, "sample.json")
    data = {
        "name": "John",
        "age": 30,
        "city": "New York",
        "hobbies": ["reading", "gaming"],
    }
    with open(json_path, "w") as f:
        json.dump(data, f)
    return json_path


@pytest.fixture
def sample_txt_file(temp_dir):
    """Create a sample text file."""
    txt_path = os.path.join(temp_dir, "sample.txt")
    with open(txt_path, "w") as f:
        f.write("This is a sample text file.\n")
        f.write("It contains multiple lines.\n")
        f.write("And some content.")
    return txt_path


@pytest.fixture
def sample_xlsx_file(temp_dir):
    """Create a sample Excel file."""
    import pandas as pd

    xlsx_path = os.path.join(temp_dir, "sample.xlsx")
    data = {
        "name": ["John", "Jane", "Bob"],
        "age": [30, 28, 35],
        "city": ["New York", "Los Angeles", "Chicago"],
    }
    df = pd.DataFrame(data)
    df.to_excel(xlsx_path, index=False)
    return xlsx_path


@pytest.fixture
def sample_pdf_file(temp_dir):
    """Create a sample PDF file."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        pdf_path = os.path.join(temp_dir, "sample.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 750, "This is a sample PDF file.")
        c.drawString(100, 730, "It contains some text content.")
        c.save()
        return pdf_path
    except ImportError:
        pytest.skip("reportlab not installed")


@pytest.fixture
def sample_docx_file(temp_dir):
    """Create a sample DOCX file."""
    from docx import Document

    docx_path = os.path.join(temp_dir, "sample.docx")
    doc = Document()
    doc.add_paragraph("This is a sample DOCX file.")
    doc.add_paragraph("It contains some text content.")
    doc.save(docx_path)
    return docx_path


@pytest.fixture
def nonexistent_file():
    """Return path to a non-existent file."""
    return "/nonexistent/path/to/file.csv"
