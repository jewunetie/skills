---
name: pdf-vision
description: Vision-based PDF reading that preserves layout, figures, tables, and visual formatting. Use this skill when reading or analyzing PDF content where visual elements matter - documents with charts, diagrams, complex tables, multi-column layouts, forms, or any PDF where text extraction would lose important information. Converts PDF pages to images and uses vision to read them, providing richer understanding than text extraction alone.
---

# PDF Vision Reader

## When to Use This Skill

Use vision-based PDF reading when:
- PDF contains figures, charts, or diagrams
- PDF has complex tables that text extraction mangles
- PDF uses multi-column layouts
- PDF contains forms or structured visual elements
- Text extraction produces garbled or incomplete results
- Precise understanding of visual layout matters

For simple text-only PDFs without visual complexity, standard text extraction (pdfplumber/pypdf) may be faster.

## Reading PDFs with Vision

### Step 1: Convert PDF to Images

```bash
# Create output directory and clean up any old images
mkdir -p /tmp/pdf_pages
rm -f /tmp/pdf_pages/page-*.png

# Convert PDF pages to PNG images (best quality for vision)
pdftoppm -png -r 150 /path/to/document.pdf /tmp/pdf_pages/page

# This creates: page-1.png, page-2.png, etc.
```

Resolution options:
- `-r 150`: Good balance of quality and file size (default)
- `-r 200`: Higher quality for dense documents
- `-r 100`: Faster processing for simple documents

### Step 2: View the Images

Use the `view` tool to examine each page image:

```
view /tmp/pdf_pages/page-1.png
view /tmp/pdf_pages/page-2.png
# ... etc
```

This provides full visual context including:
- Layout and formatting
- Tables as they visually appear
- Charts, graphs, and diagrams
- Figures and images
- Headers, footers, and page structure

### Step 3: Supplementary Text Extraction (Optional)

For precise text content or when you need searchable text alongside vision:

```python
import pdfplumber

pdf_path = "/tmp/document.pdf"  # Path to your PDF
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"--- Page {i+1} ---")
        print(text)
```

## Helper Script

The skill includes `scripts/pdf_to_images.py` (relative to the skill directory). This script handles cleanup of old images automatically:

```bash
python3 /path/to/skill/scripts/pdf_to_images.py /path/to/document.pdf
# Creates images in /tmp/pdf_pages/
```

Or with custom output directory and resolution:

```bash
python3 /path/to/skill/scripts/pdf_to_images.py /path/to/document.pdf --output /tmp/my_pdf --dpi 200
```

## Complete Workflow Example

```python
import subprocess
from pathlib import Path

def read_pdf_with_vision(pdf_path: str, output_dir: str = "/tmp/pdf_pages", dpi: int = 150):
    """Convert PDF to images for vision-based reading."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Clean up old images to avoid mixing with previous runs
    for old_image in output_path.glob("page-*.png"):
        old_image.unlink()
    
    # Convert PDF to PNG images
    subprocess.run([
        "pdftoppm", "-png", "-r", str(dpi),
        pdf_path, f"{output_dir}/page"
    ], check=True)
    
    # List generated images
    images = sorted(output_path.glob("page-*.png"))
    print(f"Generated {len(images)} page images in {output_dir}")
    return images

# Usage
images = read_pdf_with_vision("/mnt/user-data/uploads/document.pdf")
# Then use view tool on each image
```

## Quick Reference

| Task | Command |
|------|---------|
| Convert PDF to images | `pdftoppm -png -r 150 input.pdf /tmp/pdf_pages/page` |
| View single page | `view /tmp/pdf_pages/page-1.png` |
| List all page images | `ls /tmp/pdf_pages/page-*.png` |
| High-res conversion | `pdftoppm -png -r 200 input.pdf /tmp/pdf_pages/page` |
| Convert specific pages | `pdftoppm -png -r 150 -f 1 -l 5 input.pdf /tmp/pdf_pages/page` |

## Notes

- `pdftoppm` is part of poppler-utils (pre-installed)
- PNG format provides best quality for vision analysis
- Page numbering starts at 1 (page-1.png, page-2.png, etc.)
- For very large PDFs, convert in batches using `-f` (first page) and `-l` (last page) flags
- pdfplumber can supplement vision with extracted text when needed
