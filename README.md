# bun-utils

**Shared utilities for Bun's Python projects**

A collection of reusable components extracted from multiple projects to reduce code duplication and share best practices.

---

## 🎯 Purpose

When you have 7+ repos doing similar things (image handling, HTML generation, JSON I/O), you end up copying code. This library provides one place to fix bugs and add features that benefit all projects.

---

## ✨ Features

### 📸 Image Utilities (`bun_utils.images`)
- **Deduplication** - Remove duplicate images by filename
- **Statistics** - Get deduplication stats without modifying files
- **Grouping** - Find which files are duplicates of each other

### 🎨 HTML Generation (`bun_utils.html`)
- **Gallery Builder** - Create complete image galleries
- **Components** - Reusable image cards, modals, search boxes
- **Themes** - Dark/light mode support
- **Responsive** - Mobile-friendly layouts

### 📁 File Handling (`bun_utils.files`)
- **JSON I/O** - Safe reading/writing with error handling
- **Validation** - Schema validation for JSON
- **Merging** - Combine multiple JSON files

---

## 📦 Installation

### Development Install (Recommended)
```bash
# Install in editable mode - changes take effect immediately
cd ~/Documents/bun-utils
pip install -e .
```

### Regular Install
```bash
pip install ~/Documents/bun-utils
```

---

## 🚀 Quick Start

### Image Deduplication

```python
from bun_utils.images import deduplicate_by_filename

# List of image paths (might have duplicates)
images = [
    'bun_images/bun_msg123_0_photo.png',
    'bun_images/bun_msg456_0_photo.png',  # Same photo!
    'bun_images/bun_thread78_0_other.png'
]

# Remove duplicates
unique_images, removed = deduplicate_by_filename(images)

print(f"Unique: {len(unique_images)}")  # 2
print(f"Removed: {removed}")  # 1
```

### HTML Gallery

```python
from bun_utils.html import GalleryBuilder

# Create a gallery
gallery = GalleryBuilder(title="My Images", theme='dark')
gallery.add_images(['image1.png', 'image2.png'])

# Render to HTML file
html = gallery.render()
with open('gallery.html', 'w') as f:
    f.write(html)
```

### JSON Handling

```python
from bun_utils.files import read_json, write_json

# Safe read (returns None if file doesn't exist)
data = read_json('config.json', default={})

# Safe write (creates directories if needed)
write_json('output/data.json', {'key': 'value'})
```

---

## 📚 Full API

### `bun_utils.images`

#### `deduplicate_by_filename(file_list)`
Remove duplicates based on base filename.

**Args:**
- `file_list` (List[str]): List of file paths

**Returns:**
- Tuple[List[str], int]: (unique_files, duplicates_removed)

**Example:**
```python
unique, removed = deduplicate_by_filename([
    'bun_msg1_0_photo.png',
    'bun_msg2_0_photo.png',  # Duplicate!
])
# unique = ['bun_msg1_0_photo.png']
# removed = 1
```

#### `get_deduplication_stats(file_list)`
Get statistics without removing duplicates.

**Returns:**
- Dict with keys: `total_files`, `unique_names`, `duplicates`, `duplicate_rate`

#### `find_duplicate_groups(file_list)`
Group files by their base filename.

**Returns:**
- Dict[str, List[str]]: Maps base filename to list of paths

---

### `bun_utils.html`

#### `GalleryBuilder(title, theme='dark')`
Builder class for creating galleries.

**Methods:**
- `add_image(path, metadata=None)` - Add single image
- `add_images(paths)` - Add multiple images
- `render()` - Generate HTML string

**Example:**
```python
gallery = GalleryBuilder(theme='light')
gallery.add_image('photo.png', metadata={'channel': 'photos'})
html = gallery.render()
```

#### `create_image_card(path, index, total, display_name=None, metadata=None)`
Generate HTML for a single image card.

#### `create_gallery_css(theme='dark')`
Generate CSS for gallery styling.

---

### `bun_utils.files`

#### `read_json(filepath, default=None)`
Safely read JSON file.

#### `write_json(filepath, data, indent=2, create_dirs=True)`
Safely write JSON file.

#### `validate_json_schema(data, required_keys)`
Check if JSON has required keys.

#### `merge_json_files(filepaths, output_path=None)`
Merge multiple JSON files.

---

## 🔧 Used By

- **slack-bot-image-compiler** - Image deduplication, gallery generation
- **AutoScribe** - HTML generation, file handling
- **skeleton-optimizer** - JSON handling (planned)
- More repos as needed!

---

## 🤝 Contributing

This is a personal utility library, but contributions welcome!

### Adding New Utilities

1. Add to appropriate module (`images/`, `html/`, `files/`)
2. Update module's `__init__.py` to export it
3. Add docstrings and type hints
4. Test in at least 2 projects

### Guidelines

- ✅ Keep functions pure (no side effects when possible)
- ✅ Add type hints
- ✅ Write docstrings
- ✅ No external dependencies unless absolutely necessary
- ✅ Extract when used 3+ times across projects

---

## 📊 Stats

**Created:** November 7, 2025
**Current Version:** 0.1.0
**Lines of Code:** ~500
**Projects Using:** 2 (slack-export-bot, AutoScribe)
**Dependencies:** 0 external (pure Python!)

---

## 🗺️ Roadmap

### v0.2.0 (Next)
- [ ] Markdown parsing utilities
- [ ] Slack API wrappers
- [ ] Image optimization (resize, compress)

### v0.3.0 (Future)
- [ ] UI components (modals, buttons)
- [ ] Theme system
- [ ] Template engine

### v1.0.0 (Stable)
- [ ] Full test coverage
- [ ] Documentation site
- [ ] PyPI publication

---

## 📝 License

MIT License - Free to use in all your projects!

---

## 🎓 Learn More

This library demonstrates the **shared utility pattern**:
- ✅ Extract common code to one place
- ✅ Fix bugs once, benefits all projects
- ✅ Share best practices automatically
- ✅ Keep projects independent

**Not:** Monorepo, git submodules, or complex dependency management.
**Just:** Simple pip install, import, and use!

---

**Made with ❤️ for reducing code duplication**

---

## For Claude Code Instances

**Version Control Guidelines:** See [`.github/VERSION_CONTROL.md`](.github/VERSION_CONTROL.md) for complete versioning guidelines.

### Quick Reference
- **New features**: Always create feature branch (`git checkout -b feature/name`)
- **Feature complete**: Tag working state (`git tag -a v0.X.0 -m "description"`)
- **Before risky changes**: Tag current state as backup
- **Rollback**: `git checkout <tag-name>` to return to working version

### Current Version
Check latest tag: `git describe --tags --abbrev=0`

