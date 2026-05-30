"""Utility functions."""
import os
from pathlib import Path


def ensure_upload_directory(directory: str) -> str:
    """Ensure upload directory exists."""
    os.makedirs(directory, exist_ok=True)
    return directory


def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Validate if file type is allowed."""
    file_extension = Path(filename).suffix.lower().lstrip(".")
    return file_extension in allowed_types


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(file_path)
