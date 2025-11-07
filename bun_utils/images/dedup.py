#!/usr/bin/env python3
"""
Image deduplication utilities

Removes duplicate images based on filename, useful when the same
image has been posted multiple times in different messages/threads.
"""

import os
import re
from typing import List, Tuple, Dict


def deduplicate_by_filename(file_list: List[str]) -> Tuple[List[str], int]:
    """
    Remove duplicate files based on their base filename.

    Useful when you have files like:
    - bun_msg123_0_image.png
    - bun_msg456_0_image.png
    - bun_thread78_0_image.png

    All will be deduplicated to just one "image.png"

    Args:
        file_list: List of file paths

    Returns:
        Tuple of (unique_files, duplicates_removed_count)
    """
    seen_names = {}
    unique = []
    duplicates_skipped = 0

    for filepath in file_list:
        filename = os.path.basename(filepath)

        # Extract the actual filename from patterns like bun_msg123_0_name.png
        match = re.match(r'bun_(msg|thread)\d+_\d+_(.+)$', filename)
        if match:
            actual_name = match.group(2)
        else:
            actual_name = filename

        if actual_name not in seen_names:
            seen_names[actual_name] = filepath
            unique.append(filepath)
        else:
            duplicates_skipped += 1

    return unique, duplicates_skipped


def deduplicate_simple(file_list: List[str]) -> Tuple[List[str], int]:
    """
    Simple deduplication - removes exact duplicate paths.

    Args:
        file_list: List of file paths

    Returns:
        Tuple of (unique_files, duplicates_removed_count)
    """
    unique = list(set(file_list))
    duplicates_skipped = len(file_list) - len(unique)
    return unique, duplicates_skipped


def get_deduplication_stats(file_list: List[str]) -> Dict[str, int]:
    """
    Get statistics about duplicates without removing them.

    Args:
        file_list: List of file paths

    Returns:
        Dictionary with stats
    """
    seen_names = {}
    duplicate_count = 0

    for filepath in file_list:
        filename = os.path.basename(filepath)

        # Extract the actual filename from patterns like bun_msg123_0_name.png
        match = re.match(r'bun_(msg|thread)\d+_\d+_(.+)$', filename)
        if match:
            actual_name = match.group(2)
        else:
            actual_name = filename

        if actual_name not in seen_names:
            seen_names[actual_name] = 1
        else:
            seen_names[actual_name] += 1
            duplicate_count += 1

    return {
        'total_files': len(file_list),
        'unique_names': len(seen_names),
        'duplicates': duplicate_count,
        'duplicate_rate': duplicate_count / len(file_list) if file_list else 0
    }


def find_duplicate_groups(file_list: List[str]) -> Dict[str, List[str]]:
    """
    Group files by their base filename to see which are duplicates.

    Args:
        file_list: List of file paths

    Returns:
        Dictionary mapping base filename to list of full paths
    """
    groups = {}

    for filepath in file_list:
        filename = os.path.basename(filepath)

        # Extract the actual filename from patterns like bun_msg123_0_name.png
        match = re.match(r'bun_(msg|thread)\d+_\d+_(.+)$', filename)
        if match:
            actual_name = match.group(2)
        else:
            actual_name = filename

        if actual_name not in groups:
            groups[actual_name] = []
        groups[actual_name].append(filepath)

    # Only return groups with duplicates
    return {name: paths for name, paths in groups.items() if len(paths) > 1}
