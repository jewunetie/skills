#!/usr/bin/env python3
"""Convert PDF pages to PNG images for vision-based reading.

Usage:
    python3 pdf_to_images.py /path/to/document.pdf
    python3 pdf_to_images.py /path/to/document.pdf --output /tmp/my_pdf --dpi 200
    python3 pdf_to_images.py /path/to/document.pdf --first 1 --last 5  # Pages 1-5 only
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def convert_pdf_to_images(
    pdf_path: str,
    output_dir: str = "/tmp/pdf_pages",
    dpi: int = 150,
    first_page: Optional[int] = None,
    last_page: Optional[int] = None,
) -> List[Path]:
    """Convert PDF pages to PNG images using pdftoppm.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save PNG images
        dpi: Resolution in dots per inch (default 150)
        first_page: First page to convert (1-indexed, optional)
        last_page: Last page to convert (1-indexed, optional)
    
    Returns:
        List of paths to generated PNG images
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_file}")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Clean up any existing page images to avoid mixing with previous runs
    for old_image in output_path.glob("page-*.png"):
        old_image.unlink()
    
    # Build pdftoppm command
    cmd = ["pdftoppm", "-png", "-r", str(dpi)]
    
    if first_page is not None:
        cmd.extend(["-f", str(first_page)])
    if last_page is not None:
        cmd.extend(["-l", str(last_page)])
    
    cmd.extend([str(pdf_file), str(output_path / "page")])
    
    # Run conversion
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pdftoppm failed: {result.stderr}")
    
    # Find generated images
    images = sorted(output_path.glob("page-*.png"))
    return images


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to PNG images for vision-based reading"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--output", "-o",
        default="/tmp/pdf_pages",
        help="Output directory for PNG images (default: /tmp/pdf_pages)"
    )
    parser.add_argument(
        "--dpi", "-d",
        type=int,
        default=150,
        help="Resolution in DPI (default: 150, use 200 for dense documents)"
    )
    parser.add_argument(
        "--first", "-f",
        type=int,
        default=None,
        help="First page to convert (1-indexed)"
    )
    parser.add_argument(
        "--last", "-l",
        type=int,
        default=None,
        help="Last page to convert (1-indexed)"
    )
    
    args = parser.parse_args()
    
    try:
        images = convert_pdf_to_images(
            args.pdf_path,
            args.output,
            args.dpi,
            args.first,
            args.last,
        )
        if images:
            print(f"Converted {len(images)} pages to PNG images in {args.output}")
            for img in images:
                print(f"  {img}")
            print(f"\nUse 'view {images[0]}' to examine pages")
        else:
            print("Warning: No pages were generated. The PDF may be empty.", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
