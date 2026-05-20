# Operation Parameters Reference

Detailed guidance on choosing parameters for each operation.

## Geometric Operations

### rotate

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `-a/--angle` | float | required | any | Degrees counter-clockwise |

**Common values:**
- `90`: Quarter turn counter-clockwise (original top edge moves to the LEFT side)
- `180`: Upside down correction
- `270` or `-90`: Quarter turn clockwise (original top edge moves to the RIGHT side)
- Arbitrary: For slight angles, consider `deskew` instead

**Quality note:** 90/180/270 use lossless transpose. Other angles use bicubic interpolation.

### flip

| Parameter | Type | Default | Options | Notes |
|-----------|------|---------|---------|-------|
| `-d/--direction` | string | required | horizontal, vertical | Mirror axis |

**When to use:**
- `horizontal`: Content appears mirrored (text reads backward)
- `vertical`: Rarely needed; usually rotation is more appropriate

### deskew

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| (none) | - | - | - | Auto-detects angle |

**Behavior:**
- Detects angles up to ±15°
- Uses line detection (works best with text/structured content)
- Skips correction if detected angle < 0.5°
- Fills expanded areas with white

**Caveat:** The white fill is hardcoded. For dark-background images, this creates visible white borders. Workaround: invert the image, deskew, then invert back.

**When to use:** Scanned documents with slight rotation. Not for 90° rotations.

### crop

| Parameter | Type | Default | Format | Notes |
|-----------|------|---------|--------|-------|
| `--box` | string | required | L,T,R,B | Comma-separated integers |

**Box format:** `left,top,right,bottom` in pixels from top-left origin (0,0).

**Example:** `--box 100,50,600,400` extracts rectangle from (100,50) to (600,400).

**Tips:**
- Include small margin around target (10-20px)
- Get dimensions first with `info` command
- Right must be > left, bottom must be > top

### scale

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `--factor` | float | - | 0.1-4.0 | Multiplication factor |
| `--width` | int | - | 1+ | Target width in pixels |
| `--height` | int | - | 1+ | Target height in pixels |

**Usage patterns:**
- `--factor 2`: Double size (most common for detail inspection)
- `--factor 0.5`: Halve size
- `--width 800`: Scale to 800px wide, maintain aspect ratio
- `--width 800 --height 600`: Exact dimensions (may distort)

**Guidelines:**
- For text: target 30-50px character height
- Maximum useful factor: 4x (beyond just enlarges blur)
- Use LANCZOS resampling (automatic)
- **Resolution context:** When the model views the result, images with a long edge over 1568px are internally downscaled. Scaling a cropped region to ~1200-1500px on its long edge is a sweet spot: large enough for the model to resolve fine detail, small enough to avoid unnecessary downscaling.

## Tonal Operations

### brightness

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `--brightness` | float | 1.0 | 0.0-3.0 | Brightness factor |

**Values:**
- `1.0`: No change
- `1.2-1.5`: Moderate brightening (dark photos)
- `0.7-0.9`: Moderate darkening (overexposed)
- `< 0.5` or `> 2.0`: Usually too extreme

### contrast

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `--contrast-factor` | float | 1.0 | 0.0-3.0 | Contrast factor |

**Values:**
- `1.0`: No change
- `1.3-1.5`: Moderate increase (washed out images)
- `0.7-0.9`: Moderate decrease (harsh lighting)
- `> 2.0`: Usually clips highlights/shadows

**When to use:** Uniformly lit images. For varied lighting, use CLAHE instead.

### clahe

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `--clip` | float | 2.0 | 1.0-4.0 | Contrast limit |
| `--grid` | int | 8 | 4-16 | Tile grid size |

**Clip limit guidance:**
- `1.0-1.5`: Subtle enhancement
- `2.0`: Default, good for most cases
- `2.5-3.0`: Stronger enhancement (very low contrast)
- `4.0`: Maximum (may look over-processed)

**Grid size guidance:**
- `8`: Default, good balance
- `4`: Larger tiles, more global effect
- `16`: Smaller tiles, more local detail

**Best for:** Uneven lighting, shadows, backlit subjects, documents with varying illumination.

### histogram

No parameters. Applies global histogram equalization using LAB colorspace (equalizes luminance only, preserving color fidelity).

**When to use:** Uniformly lit images needing overall contrast boost. Not for images with both dark and light regions (use CLAHE instead).

### invert

No parameters. Inverts all color channels.

**When to use:**
- Light text on dark background
- Negative images
- Apply BEFORE other tonal corrections

## Detail Operations

### denoise

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `--strength` | int | 10 | 5-20 | Filter strength |

**Strength guidance:**
- `5-7`: Light noise reduction, preserves most detail
- `10`: Default, moderate noise reduction
- `15-20`: Heavy noise reduction, may blur fine detail

**Implementation detail:** Uses a bilateral filter (edge-preserving). The user-facing strength value is mapped internally to sigma values of `strength * 7.5` (so strength 10 = sigma 75). This means even moderate settings apply substantial smoothing.

**Performance note:** Bilateral filtering is computationally expensive on large images. For images above 4000px on either axis, crop to the region of interest first, or use a different enhancement (CLAHE, contrast) instead.

**Warning:** Aggressive denoising destroys fine text and detail. Start low.

### sharpen

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `--amount` | float | 1.0 | 0.5-2.0 | Sharpening strength |
| `--radius` | float | 1.0 | 0.5-3.0 | Blur radius |

**Amount guidance:**
- `0.5-0.8`: Subtle sharpening
- `1.0`: Default, moderate sharpening
- `1.2-1.5`: Noticeable sharpening
- `> 1.5`: Risk of halos and artifacts

**Radius guidance:**
- `0.5-1.0`: Fine detail sharpening
- `1.5-2.0`: Broader edge enhancement
- `> 2.0`: Can create visible halos

**Critical rules:**
1. Apply only ONCE per workflow
2. Apply AFTER scaling, not before
3. Do NOT apply to noisy images (amplifies noise)

## Specialized Operations

### binarize

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `--block-size` | int | 11 | 3-51 (odd) | Neighborhood size (enforced) |
| `--c` | int | 2 | -10 to 10 | Threshold adjustment |

**Block size guidance:**
- `7-11`: Small text, high detail
- `15-21`: Normal documents
- `31-51`: Large text, noisy backgrounds

**C value guidance:**
- `2`: Default, works for most cases
- `5-10`: If result is too light (more black)
- `-2 to 0`: If result is too dark (more white)

**Restrictions:**
- ONLY use for high-contrast printed text
- NEVER use for: photos, diagrams, handwriting, charts, shaded graphics
- Apply as LAST operation if at all

## Utility Operations

### info

| Parameter | Type | Notes |
|-----------|------|-------|
| `--json` | flag | Output as JSON |

**Returns:** size, width, height, mode, format

### exif

No parameters. Applies EXIF orientation metadata.

**When to use:** First step for photos from phones/cameras. Harmless to apply even if no EXIF data present.

## Parameter Selection Flowchart

```
Need to enhance contrast?
├── Lighting is uniform → contrast --contrast-factor 1.3-1.5
└── Lighting varies → clahe --clip 2.0

Image too dark?
├── Slightly dark → brightness --brightness 1.2
├── Very dark → brightness --brightness 1.5 + clahe
└── Shadows but bright areas OK → clahe only

Need to sharpen?
├── After scaling → sharpen --amount 1.0
├── Slightly soft → sharpen --amount 0.7
└── Very soft → sharpen --amount 1.2 (max)

Image is noisy?
├── Light noise → denoise --strength 7
├── Moderate noise → denoise --strength 10
└── Heavy noise → denoise --strength 15, accept detail loss

Need to scale up?
├── For reading text → scale --factor 2 (target 30-50px chars)
├── For detail inspection → scale --factor 2-3
└── Maximum useful → scale --factor 4
```
