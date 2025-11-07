#!/usr/bin/env python3
"""
HTML gallery generation utilities

Provides reusable components for creating image galleries with
consistent styling across projects.
"""

from urllib.parse import quote
from typing import List, Dict, Optional


def create_image_card(image_path: str, index: int, total: int,
                     display_name: Optional[str] = None,
                     metadata: Optional[Dict] = None) -> str:
    """
    Create a single image card HTML component.

    Args:
        image_path: Path to the image
        index: Image index (0-based)
        total: Total number of images
        display_name: Display name (defaults to basename)
        metadata: Optional metadata dict (channel, date, etc.)

    Returns:
        HTML string for the image card
    """
    if display_name is None:
        display_name = image_path.split('/')[-1]

    # URL encode the path for browser compatibility
    encoded_path = quote(image_path, safe='/:')

    # Build metadata string
    meta_parts = [f"Image {index + 1} of {total}"]
    if metadata:
        if 'channel' in metadata:
            meta_parts.insert(0, f"#{metadata['channel']}")
        if 'size' in metadata:
            size_mb = metadata['size'] / (1024 * 1024)
            meta_parts.append(f"{size_mb:.1f}MB")

    meta_str = " · ".join(meta_parts)

    return f'''
    <div class="image-card">
        <div class="image-container">
            <img src="{encoded_path}"
                 alt="{display_name}"
                 loading="lazy"
                 onerror="this.parentElement.parentElement.style.display='none'">
        </div>
        <div class="image-info">
            <div class="image-filename">{display_name}</div>
            <div class="image-meta">{meta_str}</div>
        </div>
    </div>
    '''


def create_modal_html() -> str:
    """
    Create the modal overlay HTML for viewing images full-size.

    Returns:
        HTML string for the modal component
    """
    return '''
    <div id="modal" class="modal" onclick="closeModal()">
        <span class="close">&times;</span>
        <div class="modal-content" onclick="event.stopPropagation()">
            <img id="modalImg">
            <div class="modal-info" id="modalInfo"></div>
        </div>
    </div>
    '''


def create_search_box(placeholder: str = "🔍 Search images...") -> str:
    """
    Create a search input component.

    Args:
        placeholder: Placeholder text

    Returns:
        HTML string for search box
    """
    return f'''
    <div class="search-box">
        <input type="text" id="searchInput" placeholder="{placeholder}">
    </div>
    '''


def create_gallery_css(theme: str = 'dark') -> str:
    """
    Generate CSS for image gallery.

    Args:
        theme: 'dark' or 'light'

    Returns:
        CSS string
    """
    if theme == 'dark':
        bg_color = '#1a1a1a'
        card_bg = '#2a2a2a'
        text_color = '#fff'
        accent_color = '#667eea'
    else:
        bg_color = '#f5f5f5'
        card_bg = '#ffffff'
        text_color = '#333'
        accent_color = '#667eea'

    return f'''
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: {bg_color};
        color: {text_color};
        padding: 20px;
    }}

    .gallery {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        max-width: 1400px;
        margin: 0 auto;
    }}

    .image-card {{
        background: {card_bg};
        border-radius: 10px;
        overflow: hidden;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        height: 420px;
        transition: transform 0.2s;
    }}

    .image-card:hover {{
        transform: translateY(-2px);
    }}

    .image-container {{
        width: 100%;
        height: 300px;
        overflow: hidden;
        background: {bg_color};
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .image-container img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }}

    .image-info {{
        padding: 15px;
        height: 120px;
        overflow: hidden;
    }}

    .image-filename {{
        font-weight: 600;
        margin-bottom: 5px;
        color: {accent_color};
        word-break: break-word;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }}

    .image-meta {{
        font-size: 0.85em;
        color: {'#888' if theme == 'dark' else '#666'};
        margin-top: 5px;
    }}

    .search-box {{
        max-width: 500px;
        margin: 0 auto 30px;
    }}

    .search-box input {{
        width: 100%;
        padding: 15px;
        background: {card_bg};
        border: 2px solid {accent_color};
        border-radius: 25px;
        color: {text_color};
        font-size: 1em;
        outline: none;
    }}

    .modal {{
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.98);
        align-items: center;
        justify-content: center;
    }}

    .modal-content {{
        margin: auto;
        max-width: 90vw;
        max-height: 90vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
    }}

    .modal-content img {{
        max-width: 90vw;
        max-height: 70vh;
        object-fit: contain;
    }}

    .close {{
        color: #fff;
        font-size: 40px;
        font-weight: bold;
        position: fixed;
        right: 30px;
        top: 10px;
        cursor: pointer;
        z-index: 10000;
        padding: 10px;
    }}

    .close:hover {{
        color: {accent_color};
    }}
    '''


class GalleryBuilder:
    """
    Builder class for creating complete HTML galleries.

    Example:
        gallery = GalleryBuilder(theme='dark')
        gallery.add_images(image_list)
        html = gallery.render()
    """

    def __init__(self, title: str = "Image Gallery", theme: str = 'dark'):
        self.title = title
        self.theme = theme
        self.images = []

    def add_image(self, path: str, metadata: Optional[Dict] = None):
        """Add a single image."""
        self.images.append({
            'path': path,
            'metadata': metadata or {}
        })

    def add_images(self, paths: List[str]):
        """Add multiple images."""
        for path in paths:
            self.add_image(path)

    def render(self) -> str:
        """Render complete HTML gallery."""
        cards_html = ""
        for idx, img in enumerate(self.images):
            cards_html += create_image_card(
                img['path'],
                idx,
                len(self.images),
                metadata=img['metadata']
            )

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>
        {create_gallery_css(self.theme)}
    </style>
</head>
<body>
    <h1 style="text-align: center; margin-bottom: 40px;">{self.title}</h1>
    {create_search_box()}
    <div class="gallery">
        {cards_html}
    </div>
    {create_modal_html()}
    <script>
        function closeModal() {{
            document.getElementById('modal').style.display = 'none';
        }}

        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.image-card');

            cards.forEach(card => {{
                const filename = card.querySelector('.image-filename').textContent.toLowerCase();
                card.style.display = filename.includes(searchTerm) ? 'flex' : 'none';
            }});
        }});

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') closeModal();
        }});
    </script>
</body>
</html>'''
