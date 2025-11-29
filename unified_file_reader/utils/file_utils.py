"""
Utility functions for file operations.

Follows DRY (Don't Repeat Yourself) principle by centralizing
common file operations used across readers.
"""

import os
from typing import Optional


def get_extension(path: str) -> str:
    """
    Extract file extension from path.

    Args:
        path: File path

    Returns:
        File extension in lowercase (e.g., ".csv")

    Raises:
        ValueError: If path is empty or invalid
    """
    if not path or not isinstance(path, str):
        raise ValueError("Path must be a non-empty string")

    _, ext = os.path.splitext(path)
    return ext.lower()


def ensure_file_exists(path: str) -> None:
    """
    Verify that a file exists at the given path.

    Args:
        path: File path to check

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If path is empty or invalid
    """
    if not path or not isinstance(path, str):
        raise ValueError("Path must be a non-empty string")

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: {path}")


def get_file_size(path: str) -> int:
    """
    Get file size in bytes.

    Args:
        path: File path

    Returns:
        File size in bytes

    Raises:
        FileNotFoundError: If file does not exist
    """
    ensure_file_exists(path)
    return os.path.getsize(path)


def is_readable(path: str) -> bool:
    """
    Check if file is readable.

    Args:
        path: File path

    Returns:
        True if file is readable, False otherwise
    """
    try:
        ensure_file_exists(path)
        return os.access(path, os.R_OK)
    except (FileNotFoundError, ValueError):
        return False
