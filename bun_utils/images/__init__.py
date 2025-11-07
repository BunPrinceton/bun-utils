"""Image handling utilities"""

from .dedup import (
    deduplicate_by_filename,
    deduplicate_simple,
    get_deduplication_stats,
    find_duplicate_groups
)

__all__ = [
    'deduplicate_by_filename',
    'deduplicate_simple',
    'get_deduplication_stats',
    'find_duplicate_groups'
]
