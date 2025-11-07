#!/usr/bin/env python3
"""
JSON file handling utilities

Safe JSON reading/writing with error handling and validation.
"""

import json
import os
from typing import Any, Optional, List


def read_json(filepath: str, default: Any = None) -> Any:
    """
    Safely read JSON file with error handling.

    Args:
        filepath: Path to JSON file
        default: Value to return if file doesn't exist or is invalid

    Returns:
        Parsed JSON data or default value
    """
    if not os.path.exists(filepath):
        return default

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return default


def write_json(filepath: str, data: Any, indent: int = 2, create_dirs: bool = True) -> bool:
    """
    Safely write JSON file with error handling.

    Args:
        filepath: Path to JSON file
        data: Data to write
        indent: JSON indentation (default 2)
        create_dirs: Create parent directories if needed

    Returns:
        True if successful, False otherwise
    """
    try:
        if create_dirs:
            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        print(f"Error: Could not write {filepath}: {e}")
        return False


def validate_json_schema(data: Any, required_keys: List[str]) -> bool:
    """
    Validate that JSON data has required keys.

    Args:
        data: Parsed JSON data
        required_keys: List of required key names

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(data, dict):
        return False

    return all(key in data for key in required_keys)


def merge_json_files(filepaths: List[str], output_path: Optional[str] = None) -> Any:
    """
    Merge multiple JSON files (assumes they're all dicts or lists).

    Args:
        filepaths: List of JSON file paths
        output_path: Optional path to write merged result

    Returns:
        Merged data
    """
    merged = None

    for filepath in filepaths:
        data = read_json(filepath)
        if data is None:
            continue

        if merged is None:
            merged = data
        elif isinstance(merged, dict) and isinstance(data, dict):
            merged.update(data)
        elif isinstance(merged, list) and isinstance(data, list):
            merged.extend(data)

    if output_path and merged is not None:
        write_json(output_path, merged)

    return merged
