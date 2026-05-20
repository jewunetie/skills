#!/usr/bin/env python3
"""
Visual Reasoning Image Operations

A comprehensive toolkit for image manipulation to enhance visual understanding.
Supports rotation, cropping, scaling, contrast enhancement, and more.

Usage:
    python image_ops.py <operation> <input_image> [options]

Examples:
    python image_ops.py rotate input.png --angle 90 --output rotated.png
    python image_ops.py crop input.png --box 100,100,500,400 --output cropped.png
    python image_ops.py clahe input.png --output enhanced.png
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import json

try:
    from PIL import Image, ImageOps, ImageEnhance, ImageFilter
    import numpy as np
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "Pillow", "numpy"])
    from PIL import Image, ImageOps, ImageEnhance, ImageFilter
    import numpy as np

try:
    import cv2
except ImportError:
    print("Installing OpenCV...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "opencv-python-headless"])
    import cv2


# =============================================================================
# Session Management
# =============================================================================

def create_session_dir():
    """Create a session directory for storing intermediate files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = Path(f"/tmp/visual_reasoning/session_{timestamp}")
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def get_next_step_path(session_dir: Path, operation: str, extension: str = ".png") -> Path:
    """Generate the next step filename in sequence."""
    existing = list(session_dir.glob("step_*"))
    step_num = len(existing)
    return session_dir / f"step_{step_num:02d}_{operation}{extension}"


# =============================================================================
# EXIF and Orientation
# =============================================================================

def fix_exif_orientation(image: Image.Image) -> tuple[Image.Image, bool]:
    """
    Apply EXIF orientation data if present.
    Returns (image, was_modified).
    """
    try:
        exif_data = image.getexif()
        # EXIF orientation tag is 0x0112 (274)
        has_orientation = 274 in exif_data and exif_data[274] != 1
        fixed = ImageOps.exif_transpose(image)
        return fixed, has_orientation
    except Exception:
        return image, False


# =============================================================================
# Geometric Operations
# =============================================================================

def rotate_image(image: Image.Image, angle: float, expand: bool = True) -> Image.Image:
    """
    Rotate image by specified angle (degrees, counter-clockwise).
    Common values: 90, 180, 270 (or -90)
    
    Args:
        image: Input PIL Image
        angle: Rotation angle in degrees (counter-clockwise)
        expand: If True, expand output to fit rotated image
    """
    # For exact 90-degree rotations, use transpose for better quality
    if angle == 90:
        return image.transpose(Image.Transpose.ROTATE_90)
    elif angle == 180:
        return image.transpose(Image.Transpose.ROTATE_180)
    elif angle == 270 or angle == -90:
        return image.transpose(Image.Transpose.ROTATE_270)
    else:
        # Arbitrary angle rotation
        return image.rotate(angle, expand=expand, resample=Image.Resampling.BICUBIC)


def flip_image(image: Image.Image, direction: str) -> Image.Image:
    """
    Flip image horizontally or vertically.
    
    Args:
        image: Input PIL Image
        direction: 'horizontal' or 'vertical'
    """
    if direction == "horizontal":
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    else:
        raise ValueError(f"Invalid flip direction: {direction}. Use 'horizontal' or 'vertical'.")


def deskew_image(image: Image.Image, max_angle: float = 15.0) -> tuple[Image.Image, float]:
    """
    Auto-detect and correct small skew angles (for scanned documents).
    
    Args:
        image: Input PIL Image
        max_angle: Maximum angle to correct (default 15 degrees)
    
    Returns:
        (corrected_image, detected_angle)
    """
    # Convert to grayscale numpy array
    if image.mode != 'L':
        gray = image.convert('L')
    else:
        gray = image
    
    img_array = np.array(gray)
    
    # Use OpenCV to detect lines and estimate skew
    edges = cv2.Canny(img_array, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    
    if lines is None or len(lines) == 0:
        return image, 0.0
    
    # Calculate angles of detected lines
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 - x1 != 0:  # Avoid division by zero
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            # Only consider near-horizontal lines
            if abs(angle) < max_angle:
                angles.append(angle)
    
    if not angles:
        return image, 0.0
    
    # Use median angle for robustness
    median_angle = np.median(angles)
    
    if abs(median_angle) < 0.5:  # Skip if angle is negligible
        return image, 0.0
    
    # Rotate to correct skew
    corrected = image.rotate(median_angle, expand=True, resample=Image.Resampling.BICUBIC, fillcolor='white')
    return corrected, median_angle


def crop_image(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    """
    Crop image to specified box.
    
    Args:
        image: Input PIL Image
        box: (left, top, right, bottom) coordinates
    """
    return image.crop(box)


def scale_image(image: Image.Image, factor: float = None, width: int = None, height: int = None) -> Image.Image:
    """
    Scale image by factor or to specific dimensions.
    
    Args:
        image: Input PIL Image
        factor: Scale factor (e.g., 2.0 for 2x)
        width: Target width (maintains aspect ratio if height not specified)
        height: Target height (maintains aspect ratio if width not specified)
    """
    original_width, original_height = image.size
    
    if factor is not None:
        new_width = int(original_width * factor)
        new_height = int(original_height * factor)
    elif width is not None and height is not None:
        new_width, new_height = width, height
    elif width is not None:
        new_width = width
        new_height = int(original_height * (width / original_width))
    elif height is not None:
        new_height = height
        new_width = int(original_width * (height / original_height))
    else:
        raise ValueError("Must specify factor, width, height, or both width and height")
    
    return image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)


# =============================================================================
# Tonal Corrections
# =============================================================================

def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust image brightness.
    
    Args:
        image: Input PIL Image
        factor: Brightness factor (1.0 = original, >1 = brighter, <1 = darker)
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust image contrast.
    
    Args:
        image: Input PIL Image
        factor: Contrast factor (1.0 = original, >1 = more contrast, <1 = less)
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def apply_clahe(image: Image.Image, clip_limit: float = 2.0, grid_size: int = 8) -> Image.Image:
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE).
    Best for images with varying lighting across regions.
    
    Args:
        image: Input PIL Image
        clip_limit: Contrast limit (default 2.0, range 1.0-4.0)
        grid_size: Size of grid for local histogram (default 8)
    """
    # Convert to numpy array
    img_array = np.array(image)
    
    # Handle different image modes
    if len(img_array.shape) == 2:
        # Grayscale
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
        result = clahe.apply(img_array)
    elif img_array.shape[2] == 3:
        # RGB - convert to LAB, apply CLAHE to L channel
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    elif img_array.shape[2] == 4:
        # RGBA - process RGB, preserve alpha
        rgb = img_array[:, :, :3]
        alpha = img_array[:, :, 3]
        lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        rgb_result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        result = np.dstack((rgb_result, alpha))
    else:
        raise ValueError(f"Unsupported image format with {img_array.shape[2]} channels")
    
    return Image.fromarray(result)


def histogram_equalize(image: Image.Image) -> Image.Image:
    """
    Apply global histogram equalization.
    Best for uniformly lit images needing overall contrast boost.
    Uses LAB colorspace to equalize luminance only, preserving color fidelity.
    """
    img_array = np.array(image)

    if len(img_array.shape) == 2:
        # Grayscale - equalize directly
        return Image.fromarray(cv2.equalizeHist(img_array))
    elif img_array.shape[2] == 4:
        # RGBA - equalize L channel in LAB, preserve alpha
        rgb = img_array[:, :, :3]
        alpha = img_array[:, :, 3]
        lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
        lab[:, :, 0] = cv2.equalizeHist(lab[:, :, 0])
        rgb_result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        result = np.dstack((rgb_result, alpha))
        return Image.fromarray(result)
    else:
        # RGB - equalize L channel in LAB to avoid color shifts
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        lab[:, :, 0] = cv2.equalizeHist(lab[:, :, 0])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        return Image.fromarray(result)


def invert_image(image: Image.Image) -> Image.Image:
    """
    Invert image colors (for light-on-dark to dark-on-light conversion).
    Palette-mode images are converted to RGB first (palette info is lost).
    """
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb = Image.merge('RGB', (r, g, b))
        inverted_rgb = ImageOps.invert(rgb)
        r, g, b = inverted_rgb.split()
        return Image.merge('RGBA', (r, g, b, a))
    elif image.mode in ('L', 'RGB'):
        return ImageOps.invert(image)
    elif image.mode == 'P':
        # Palette mode: convert to RGB first, losing palette info
        print("Warning: converting palette-mode image to RGB for inversion")
        return ImageOps.invert(image.convert('RGB'))
    elif image.mode == 'LA':
        # Grayscale with alpha
        l, a = image.split()
        inverted_l = ImageOps.invert(l)
        return Image.merge('LA', (inverted_l, a))
    else:
        print(f"Warning: converting {image.mode} image to RGB for inversion")
        return ImageOps.invert(image.convert('RGB'))


# =============================================================================
# Detail Refinement
# =============================================================================

def denoise_image(image: Image.Image, strength: int = 10) -> Image.Image:
    """
    Apply denoising using bilateral filter (preserves edges).
    
    Args:
        image: Input PIL Image
        strength: Denoising strength (default 10, range 5-20)
    """
    img_array = np.array(image)
    
    if len(img_array.shape) == 2:
        # Grayscale
        denoised = cv2.bilateralFilter(img_array, d=9, sigmaColor=strength*7.5, sigmaSpace=strength*7.5)
    elif img_array.shape[2] == 4:
        # RGBA - denoise RGB, preserve alpha
        rgb = img_array[:, :, :3]
        alpha = img_array[:, :, 3]
        denoised_rgb = cv2.bilateralFilter(rgb, d=9, sigmaColor=strength*7.5, sigmaSpace=strength*7.5)
        denoised = np.dstack((denoised_rgb, alpha))
    else:
        # RGB or other 3-channel
        denoised = cv2.bilateralFilter(img_array, d=9, sigmaColor=strength*7.5, sigmaSpace=strength*7.5)
    
    return Image.fromarray(denoised)


def sharpen_image(image: Image.Image, amount: float = 1.0, radius: float = 1.0) -> Image.Image:
    """
    Apply unsharp mask sharpening.
    
    Args:
        image: Input PIL Image
        amount: Sharpening amount (default 1.0, range 0.5-2.0)
        radius: Blur radius for unsharp mask (default 1.0)
    
    Warning: Apply only once. Multiple applications create artifacts.
    """
    # PIL's UnsharpMask: radius, percent (amount*100), threshold
    return image.filter(ImageFilter.UnsharpMask(radius=radius, percent=int(amount * 100), threshold=0))


# =============================================================================
# Specialized Transforms
# =============================================================================

def binarize_image(image: Image.Image, block_size: int = 11, c: int = 2) -> Image.Image:
    """
    Convert to binary (black and white) using adaptive thresholding.
    
    WARNING: Only use for high-contrast printed text.
    Destroys grayscale information - never use on photos, diagrams, or handwriting.
    
    Args:
        image: Input PIL Image
        block_size: Size of neighborhood for threshold calculation (must be odd, >= 3)
        c: Constant subtracted from mean (default 2)
    """
    # Validate block_size
    if block_size < 3 or block_size > 51 or block_size % 2 == 0:
        raise ValueError(f"block_size must be an odd number between 3 and 51, got {block_size}")
    
    # Convert to grayscale
    if image.mode != 'L':
        gray = image.convert('L')
    else:
        gray = image
    
    img_array = np.array(gray)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        img_array, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size, c
    )
    
    return Image.fromarray(binary)


# =============================================================================
# Utility Functions
# =============================================================================

def get_image_info(image: Image.Image) -> dict:
    """Get basic information about an image."""
    return {
        "size": image.size,
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "format": image.format,
    }


def load_image(path: str) -> Image.Image:
    """Load an image from path."""
    return Image.open(path)


def save_image(image: Image.Image, path: str, quality: int = 95):
    """Save an image to path."""
    path = Path(path)
    
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Handle format-specific saving
    if path.suffix.lower() in ['.jpg', '.jpeg']:
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(path, quality=quality)
    elif path.suffix.lower() == '.png':
        image.save(path)
    else:
        image.save(path)
    
    return str(path)


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Visual Reasoning Image Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Operations:
  info          Get image information
  exif          Fix EXIF orientation
  rotate        Rotate image (90, 180, 270, or arbitrary angle)
  flip          Flip image (horizontal/vertical)
  deskew        Auto-correct small skew angles
  crop          Crop to specified region
  scale         Scale by factor or to dimensions
  brightness    Adjust brightness
  contrast      Adjust contrast
  clahe         Apply CLAHE (local contrast enhancement)
  histogram     Apply global histogram equalization
  invert        Invert colors
  denoise       Remove noise
  sharpen       Sharpen image
  binarize      Convert to black and white (text only!)

Examples:
  %(prog)s info input.png
  %(prog)s rotate input.png -a 90 -o rotated.png
  %(prog)s crop input.png --box 100,100,500,400 -o cropped.png
  %(prog)s clahe input.png --clip 2.0 -o enhanced.png
  %(prog)s scale input.png --factor 2 -o larger.png
        """
    )
    
    parser.add_argument("operation", help="Operation to perform")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", help="Output image path")
    parser.add_argument("-a", "--angle", type=float, help="Rotation angle in degrees")
    parser.add_argument("-d", "--direction", choices=["horizontal", "vertical"], help="Flip direction")
    parser.add_argument("--box", help="Crop box as left,top,right,bottom")
    parser.add_argument("--factor", type=float, help="Scale factor")
    parser.add_argument("--width", type=int, help="Target width")
    parser.add_argument("--height", type=int, help="Target height")
    parser.add_argument("--brightness", type=float, default=1.0, help="Brightness factor (default 1.0)")
    parser.add_argument("--contrast-factor", type=float, default=1.0, help="Contrast factor (default 1.0)")
    parser.add_argument("--clip", type=float, default=2.0, help="CLAHE clip limit (default 2.0)")
    parser.add_argument("--grid", type=int, default=8, help="CLAHE grid size (default 8)")
    parser.add_argument("--strength", type=int, default=10, help="Denoise strength (default 10)")
    parser.add_argument("--amount", type=float, default=1.0, help="Sharpen amount (default 1.0)")
    parser.add_argument("--radius", type=float, default=1.0, help="Sharpen radius (default 1.0)")
    parser.add_argument("--block-size", type=int, default=11, help="Binarize block size (default 11)")
    parser.add_argument("--c", type=int, default=2, help="Binarize constant (default 2)")
    parser.add_argument("--session", help="Session directory path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Load image
    try:
        image = load_image(args.input)
    except Exception as e:
        print(f"Error loading image: {e}", file=sys.stderr)
        sys.exit(1)
    
    result = None
    metadata = {}
    
    # Perform operation
    op = args.operation.lower()
    
    if op == "info":
        info = get_image_info(image)
        if args.json:
            print(json.dumps(info))
        else:
            for key, value in info.items():
                print(f"{key}: {value}")
        sys.exit(0)
    
    elif op == "exif":
        result, was_modified = fix_exif_orientation(image)
        metadata["exif_modified"] = was_modified
    
    elif op == "rotate":
        if args.angle is None:
            print("Error: --angle required for rotate operation", file=sys.stderr)
            sys.exit(1)
        result = rotate_image(image, args.angle)
        metadata["angle"] = args.angle
    
    elif op == "flip":
        if args.direction is None:
            print("Error: --direction required for flip operation", file=sys.stderr)
            sys.exit(1)
        result = flip_image(image, args.direction)
        metadata["direction"] = args.direction
    
    elif op == "deskew":
        result, detected_angle = deskew_image(image)
        metadata["detected_angle"] = detected_angle
    
    elif op == "crop":
        if args.box is None:
            print("Error: --box required for crop operation", file=sys.stderr)
            sys.exit(1)
        try:
            box = tuple(map(int, args.box.split(",")))
            if len(box) != 4:
                raise ValueError("Box must have 4 values")
        except Exception as e:
            print(f"Error parsing box: {e}", file=sys.stderr)
            sys.exit(1)
        result = crop_image(image, box)
        metadata["box"] = box
    
    elif op == "scale":
        if args.factor is None and args.width is None and args.height is None:
            print("Error: --factor, --width, or --height required for scale operation", file=sys.stderr)
            sys.exit(1)
        result = scale_image(image, factor=args.factor, width=args.width, height=args.height)
        metadata["original_size"] = image.size
        metadata["new_size"] = result.size
    
    elif op == "brightness":
        result = adjust_brightness(image, args.brightness)
        metadata["factor"] = args.brightness
    
    elif op == "contrast":
        result = adjust_contrast(image, args.contrast_factor)
        metadata["factor"] = args.contrast_factor
    
    elif op == "clahe":
        result = apply_clahe(image, clip_limit=args.clip, grid_size=args.grid)
        metadata["clip_limit"] = args.clip
        metadata["grid_size"] = args.grid
    
    elif op == "histogram":
        result = histogram_equalize(image)
    
    elif op == "invert":
        result = invert_image(image)
    
    elif op == "denoise":
        result = denoise_image(image, strength=args.strength)
        metadata["strength"] = args.strength
    
    elif op == "sharpen":
        result = sharpen_image(image, amount=args.amount, radius=args.radius)
        metadata["amount"] = args.amount
        metadata["radius"] = args.radius
    
    elif op == "binarize":
        result = binarize_image(image, block_size=args.block_size, c=args.c)
        metadata["block_size"] = args.block_size
        metadata["c"] = args.c
    
    else:
        print(f"Unknown operation: {op}", file=sys.stderr)
        sys.exit(1)
    
    # Save result
    if result is not None:
        if args.output:
            output_path = args.output
        elif args.session:
            session_dir = Path(args.session)
            session_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(get_next_step_path(session_dir, op))
        else:
            # Default: same directory with operation suffix
            input_path = Path(args.input)
            output_path = str(input_path.parent / f"{input_path.stem}_{op}{input_path.suffix}")
        
        saved_path = save_image(result, output_path)
        
        output_info = {
            "operation": op,
            "input": args.input,
            "output": saved_path,
            "output_size": result.size,
            **metadata
        }
        
        if args.json:
            print(json.dumps(output_info))
        else:
            print(f"Saved: {saved_path}")
            print(f"Size: {result.size[0]}x{result.size[1]}")
            for key, value in metadata.items():
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()
