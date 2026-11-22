# Known Issues & Limitations

A practical look at current limitations, edge cases, and future plans for `unified-file-reader`.

---

## 1. Large Files Are Loaded Wholly into Memory
- **Current Behavior**: When you read a file (like a CSV or Excel spreadsheet), the entire dataset is parsed and loaded into RAM before returning to your code.
- **The Limitation**: If you're trying to read a 4 GB CSV or a massive Excel sheet on a machine with limited memory, Python will consume large amounts of RAM and could raise a `MemoryError`.
- **Workaround / Roadmap**: For standard document and data workloads (under a few hundred megabytes), this is very fast. For massive datasets, we plan to introduce an optional streaming iterator (e.g. `read_file_stream(path, chunksize=...)`) in an upcoming release.

---

## 2. Multi-Sheet Excel Workbooks
- **Current Behavior**: `read_file("workbook.xlsx")` defaults to reading only the first active sheet.
- **The Limitation**: Additional tabs in a multi-sheet spreadsheet are ignored by default.
- **Workaround / Roadmap**: If you need multi-sheet support today, you can subclass `ExcelReader` or use `pandas` directly. An upcoming release will add support for passing a `sheet_name` argument.

---

## 3. Scanned or Image-Only PDFs
- **Current Behavior**: `PDFReader` extracts text streams using `pypdf`.
- **The Limitation**: If a PDF is a scanned picture of paper (raster image) without an underlying digital text layer, the reader will return an empty string. The library does not bundle heavy optical character recognition (OCR) engines like Tesseract to keep installations lightweight and fast.
- **Workaround**: If your project regularly processes scanned documents, implement a custom reader integrating OCR (e.g., `pytesseract` or `easyocr`) and register it using `register_reader()`.

---

## 4. Complex Word Document Layouts (.docx)
- **Current Behavior**: `DOCXReader` extracts text from paragraph elements (`doc.paragraphs`).
- **The Limitation**: Content nested inside complex tables, header/footer regions, or text boxes inside `.docx` files is currently skipped.
- **Workaround / Roadmap**: We plan to enhance `DOCXReader` to iterate through both paragraphs and table cells in a future update.

---

## 5. Exotic File Encodings
- **Current Behavior**: Text and CSV readers automatically attempt `UTF-8` and fall back to `Latin-1` upon encountering decoding errors.
- **The Limitation**: Files using regional encodings (like `Shift-JIS` for Japanese or `GB2312` for Simplified Chinese) will raise a decoding error.
- **Workaround**: Convert the file to UTF-8 before reading, or register a small custom reader configured with your target encoding.
