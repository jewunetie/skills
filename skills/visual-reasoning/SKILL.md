---
name: visual-reasoning
description: Iterative image manipulation for enhanced visual understanding. Use when you cannot extract information from an image due to orientation, scale, quality, or format issues. Provides rotation, cropping, scaling, contrast enhancement, and more. Trigger this skill whenever image content is unreadable, too small, rotated, low-contrast, or otherwise obstructed, even if the user does not explicitly ask for image processing.
---

# Visual Reasoning Skill

A framework for iterative image manipulation to enhance visual understanding. When you cannot extract needed information from an image, use this skill to systematically transform the image until the information becomes accessible.

## When to Use This Skill

Use this skill when:
- Text in an image is too small, rotated, or low-contrast to read
- Important details are obscured by poor image quality
- You need to inspect a specific region of a larger image
- Document scans are skewed or have uneven lighting
- Light text on dark backgrounds is hard to process

Do NOT use this skill when:
- You can already extract the needed information from the image as-is
- The image quality issues are fundamental (e.g., completely out of focus, corrupted)
- The user is asking about image aesthetics rather than information extraction

## Reference Files

This skill includes two reference files for detailed guidance. Read them as needed:

- **`references/parameters.md`** -- Read when you need detailed parameter tuning guidance for any operation (recommended ranges, edge cases, quality tradeoffs).
- **`references/quick_reference.md`** -- A condensed cheat sheet of commands and decision trees. Useful for quick lookups mid-workflow. Do not read both this and the full SKILL.md; they cover overlapping content.

## Quick Start

```bash
# Check what operations are available
python scripts/image_ops.py --help

# Basic operations
python scripts/image_ops.py rotate input.png -a 90 -o output.png
python scripts/image_ops.py crop input.png --box 100,100,500,400 -o output.png
python scripts/image_ops.py clahe input.png -o output.png
python scripts/image_ops.py scale input.png --factor 2 -o output.png
```

## Reasoning Framework

### Step 1: Initial Assessment

**First question:** Can I already extract the needed information from this image as-is?

- If **YES**: respond directly, no manipulation needed
- If **PARTIALLY**: read what you can from the full image first (the surrounding context helps interpret ambiguous regions), then crop and enhance only the unreadable portions. Use what you learned from the full-image pass to interpret the enhanced crops. See the two-pass pattern below.
- If **NO**: proceed to diagnosis

**Two-pass pattern (for partial readability):**
```
Pass 1: Read the FULL image. Record what you can extract and what you cannot.
         The full image provides layout context (section headings, column
         structure, spatial relationships) that helps interpret details.

Pass 2: Crop ONLY the unreadable regions. Enhance and re-examine those crops.
         Use context from Pass 1 to resolve ambiguities in the enhanced crop.
```

This is important because of how vision models work. The model divides images into small patches (~14-16px squares), each becoming one visual token. Cropping to a smaller region allocates the full token budget to that region, giving finer detail per patch. But cropping also removes surrounding context that helps the model interpret what it reads. The two-pass approach gets the best of both: context from the full image, detail from the crop.

**Diagnostic questions (when full extraction fails):**
1. What specific information am I trying to extract?
2. What is preventing successful extraction?
   - **Orientation problem**: Content is rotated, flipped, or upside-down
   - **Scale problem**: Target details are too small to read/see clearly
   - **Quality problem**: Low contrast, noise, blur, over/underexposure
   - **Focus problem**: Target is a small region within a larger image
   - **Format problem**: Light text on dark background

### Step 2: Pre-Processing

Before any manipulation:

```bash
# 1. Create working directory and set variable
SESSION_DIR="/tmp/visual_reasoning/session_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SESSION_DIR"

# 2. Copy original to working directory (never modify the original)
cp input.png "$SESSION_DIR/step_00_original.png"

# 3. Fix EXIF orientation if present (photos from phones/cameras)
python scripts/image_ops.py exif "$SESSION_DIR/step_00_original.png" -o "$SESSION_DIR/step_01_exif.png"

# 4. Check image dimensions (useful for planning crop coordinates and judging if scaling is needed)
python scripts/image_ops.py info "$SESSION_DIR/step_01_exif.png"
```

**Format note:** The workflow uses `.png` for all intermediate files because PNG is lossless. If the original is a JPEG, WebP, or other format, the first copy converts it to PNG. This avoids recompression artifacts across steps. The tradeoff is larger file sizes for photo-heavy images.

**Understanding the 1568px downscale threshold:** When Claude receives an image, it internally scales it down if the long edge exceeds 1568 pixels (preserving aspect ratio) before dividing it into patches for analysis. A 4000x3000 phone photo becomes roughly 1568x1176 before the model ever sees it, losing fine detail. Cropping to a smaller region *before* sending it to the model is most impactful for images above this threshold, because it means the region of interest gets the full resolution budget instead of being downscaled with everything else. For images already under 1568px on both edges, cropping still helps by removing irrelevant patches (desk background, margins) but the resolution benefit is smaller.

**Estimating crop coordinates:** Use `info` to get the image dimensions. Then estimate where your target region falls proportionally. For example, if the image is 624x1090 and the document fills roughly the center 90% of the frame, the document runs from about (30, 55) to (594, 1035). If your target text is in the bottom-right quadrant of the document, estimate roughly (310, 545) to (594, 1035). When uncertain, crop generously first (include more area than you think you need), view the result, then tighten with a second crop if needed. Precise coordinates are not necessary -- the model's patches are 14-16px squares, so being off by 10-20px is fine.

### Step 3: Choose Operations

Use this table to map observed problems to operations:

| Observed Problem | Operation | Command Example |
|------------------|-----------|-----------------|
| Content upside down | Rotate 180 degrees | `rotate -a 180` |
| Content sideways (original top is now on the right edge) | Rotate 90 degrees CCW | `rotate -a 90` |
| Content sideways (original top is now on the left edge) | Rotate 270 degrees CCW | `rotate -a 270` |
| Content mirrored | Flip | `flip -d horizontal` |
| Text slightly tilted (less than 15 degrees) | Deskew | `deskew` |
| Target region too small | Crop then Scale | `crop --box L,T,R,B` then `scale --factor 2` |
| Low contrast (varying lighting) | CLAHE | `clahe --clip 2.0` |
| Low contrast (uniform lighting) | Contrast | `contrast --contrast-factor 1.5` |
| Too dark | Brightness | `brightness --brightness 1.3` |
| Too bright | Brightness | `brightness --brightness 0.7` |
| Grainy/noisy | Denoise | `denoise --strength 10` |
| Slightly blurry | Sharpen | `sharpen --amount 1.0` |
| Light text on dark | Invert | `invert` |

**"Zooming in"** is not a separate operation. It means: crop to the region of interest, then scale up. Use this term consistently when communicating with users.

### Step 4: Operation Ordering

When multiple operations are needed, follow this sequence. The rationale for each ordering constraint is given inline.

```
STEP 0: METADATA
   └── Fix EXIF orientation
       Why: The image may appear rotated but is actually correctly oriented
       once EXIF data is applied. Always do this first for photos.

STEP 1: GEOMETRIC CORRECTIONS
   ├── Rotation (90, 180, 270 degrees)
   ├── Flip (horizontal/vertical)
   └── Deskew (small angle correction)
       Why: Some enhancement filters are orientation-sensitive, and working
       on correctly oriented content makes crop coordinates easier to specify.

STEP 2: REGION SELECTION
   ├── Crop (extract region of interest)
   └── Scale (enlarge for detail)
       Why: Processing a smaller cropped region is faster and allows
       enhancements to target exactly the area that matters.

STEP 3: FORMAT CORRECTIONS
   └── Invert (light-on-dark to dark-on-light)
       Why: Tonal correction algorithms assume dark-on-light content.
       Inverting first ensures they work correctly.

STEP 4: TONAL CORRECTIONS
   ├── Brightness adjustment
   ├── Contrast adjustment
   └── CLAHE (local contrast)

STEP 5: DETAIL REFINEMENT
   ├── Denoise (if noisy)
   └── Sharpen (if soft -- apply LAST)
       Why: Sharpening amplifies noise, so always denoise first.
       Sharpening should also come after scaling because scaling
       introduces softness that sharpening can correct.

STEP 6: SPECIALIZED (use with caution)
   └── Binarize (ONLY for clean printed text)
       Why: Binarization destroys all grayscale information and is
       irreversible. Only use as a last step for high-contrast printed text.
```

### Step 5: File Management

**Directory structure:**
```
/tmp/visual_reasoning/
└── session_{timestamp}/
    ├── step_00_original.png
    ├── step_01_exif.png
    ├── step_02_rotated.png
    ├── step_03_cropped.png
    └── ...
```

**Rules and rationale:**
- Never modify the original file. You may need to restart from scratch if an operation sequence degrades quality.
- Save after each operation with a descriptive name. This creates a clear audit trail and makes it easy to revert to any prior state.
- If an operation makes things worse, revert to the previous step's file as input for the next attempt.
- Keep all intermediate files until the task is complete. They cost little and enable backtracking.

You can also use the `--session` flag to auto-name files in sequence:
```bash
python scripts/image_ops.py rotate input.png -a 90 --session "$SESSION_DIR"
# Saves as $SESSION_DIR/step_XX_rotate.png with auto-incrementing number
```

### Step 6: Iteration Control

**Maximum iterations:** 5 operations per image (not counting the EXIF fix).

**Stop when ANY of these is true:**
1. Target information successfully extracted.
2. No improvement after the last 2 consecutive operations. Continuing to apply operations without measurable progress wastes time and risks degradation.
3. Image quality has degraded compared to a previous step.
4. You have tried 3 different operation sequences for the same problem without success. At this point the limitation is likely in the source image, not the processing.
5. Reached the maximum of 5 operations.

**Anti-patterns to avoid:**
- Rotating multiple times without checking orientation after each rotation. Always view the result before deciding on further rotation.
- Applying sharpen more than once. Each application amplifies artifacts from the previous pass, creating halos and ringing.
- Scaling beyond 4x the original size. Beyond this, interpolation just enlarges blur without adding real detail.
- Aggressive denoising (strength above 15). High denoising destroys fine text strokes and thin lines.
- Binarizing photos, diagrams, or handwriting. These contain important grayscale gradients that binarization destroys.

### Step 7: Feedback Loop

```
START
  │
  ▼
ASSESS: Can I complete the task now? ◄─────────────┐
  │                                                 │
  ├── YES → Respond with findings (done)            │
  │                                                 │
  └── NO                                            │
        │                                           │
        ▼                                           │
     DIAGNOSE: What's preventing extraction?        │
        │                                           │
        ▼                                           │
     SELECT: Choose ONE operation                   │
        │                                           │
        ▼                                           │
     COMMUNICATE: State what you're doing and why   │
        │                                           │
        ▼                                           │
     APPLY: Execute operation, save result          │
        │                                           │
        ▼                                           │
     VIEW: Examine the result                       │
        │                                           │
        ▼                                           │
     EVALUATE: Better / Same / Worse?               │
        │                                           │
        └───────────────────────────────────────────┘

If SAME: try a different operation for the same problem (counts toward your 5-op limit)
If WORSE: revert to the previous step file and try an alternative approach
```

### Step 8: Error Handling

If `image_ops.py` returns an error:
- **Bad crop coordinates** (e.g., right < left, coordinates outside image): Use `info` to check image dimensions, then recalculate the box.
- **File not found**: Verify the path. Check that the previous step actually saved successfully.
- **Out of memory**: The image may be too large for the operation. Try cropping to a smaller region first, or scaling down before applying expensive operations like denoise.
- **Unsupported format**: Convert the image to PNG first by loading and re-saving it.
- **Any other error**: Report the error message to the user and suggest they provide the image in a different format or resolution.

### Task-Specific Heuristics

**OCR / Printed Text:**
```
Deskew → Scale (target 30-50px character height) → CLAHE → Binarize (optional)
- Check for light-on-dark first; if so, invert before other steps
- Binarize only for clean printed text with high contrast
- To estimate character height: use `info` to get image dimensions,
  visually estimate what fraction of the image height a text line occupies,
  and multiply. If characters are ~20px tall, scale by 2x to reach ~40px.
```

**Handwritten Notes / Whiteboards:**
```
Rotation → Crop → CLAHE → Light sharpen
- Do NOT binarize (destroys stroke width variations that aid readability)
- CLAHE handles uneven lighting well (common with whiteboards)
```

**Diagrams / Charts:**
```
Rotation → Crop → Contrast adjustment
- Preserve colors (don't binarize)
- Be careful with CLAHE on solid color fills (can create unwanted texture)
```

**Detail Inspection:**
```
Crop tightly → Scale 2-4x → Light sharpen
- Don't scale beyond 4x (just enlarges existing blur)
- Sharpen after scaling, not before
```

**Photos:**
```
EXIF orientation → Rotation if needed → CLAHE for dark areas
- Minimal processing usually produces the best results
```

**Document in Photo (photo of a printed form, letter, sign, etc.):**
```
EXIF fix → Crop to document boundaries → Then work on sub-regions

This is the most common input type. The key challenge is that the photo
contains both the document AND irrelevant background (desk, hands, other
objects). Background pixels waste the model's token budget without
contributing to reading the content.

Step 1: Crop to the document edges first, removing desk/background.
        This is a "framing crop," not a "detail crop." Be generous --
        include the full document with small margins.

Step 2: Assess the cropped document. Can you read it now?
        - If YES: respond directly.
        - If PARTIALLY: identify unreadable regions (e.g., small text in
          a corner, a dense checklist, a faded section).

Step 3: For each unreadable region, crop to THAT region from the
        document-level image, scale up, and enhance as needed.

Common sub-patterns:
- Forms with multiple sections: crop each section separately
- Two-column layouts: crop left and right columns independently
- Headers with small text: crop the header strip and scale 2-3x
- Dense checklists: crop the checklist area, scale, and use CLAHE
```

### Step 9: Reporting Limitations

When manipulation does not help, report honestly and suggest user actions:

**Template:**
```
"I attempted [operations] but [specific limitation].
This appears to be because [diagnosis].

To help me extract this information, you could:
- [Actionable suggestion 1]
- [Actionable suggestion 2]"
```

**Common limitations and suggestions:**

| Limitation | User Suggestions |
|------------|------------------|
| Text still blurry after enhancement | "Provide a higher resolution image" or "Take a closer photo" |
| Cannot determine correct orientation | "Which way is up in this image?" |
| Content obscured by glare | "Retake photo at different angle" |
| Handwriting illegible | "Can you transcribe the key portions?" |
| Multiple overlapping elements | "Can you crop to just the section you need?" |

### Handling Image Size and Resolution

**How the model sees images:** Claude divides images into patches of ~14-16px each. The total number of patches (visual tokens) determines how much detail the model can perceive. Images with a long edge over 1568px are downscaled before patching, which means fine details in large images get compressed. The token cost formula is approximately: `tokens = (width * height) / 750`, capped at ~1600 tokens.

**When cropping helps most:**
- **Large photos (long edge > 1568px):** High impact. The image is being downscaled before the model sees it. Cropping to the relevant region lets that region use the full resolution budget. A 4000x3000 phone photo downscaled to 1568x1176 gives each patch ~9 original pixels of detail. Cropping to a 1000x800 region first means no downscaling at all, and each patch covers ~4 original pixels -- more than double the effective detail.
- **Medium images (both edges under 1568px):** Moderate impact. No downscaling occurs, but cropping still removes irrelevant patches (background, margins) and lets enhancements target the area that matters.
- **Small images (under 400px on any edge):** Low impact or counterproductive. Very small images under 200px on any edge degrade model performance. Do not crop small images further; scale up first if needed.

**Performance considerations:**
- If `info` reports dimensions above 4000px on either axis, crop to the region of interest before applying any enhancement. The `denoise` bilateral filter is especially slow on large images.
- Do not scale up images that are already large. If details are unreadable at full resolution, the source lacks the information.
- When you need the full image enhanced without cropping, prefer CLAHE or contrast over denoise for speed.

## Operation Reference

### Geometric Operations

**rotate**: Rotate image by angle
```bash
python scripts/image_ops.py rotate input.png -a 90 -o output.png
# -a/--angle: degrees counter-clockwise (90, 180, 270 for exact; any float for arbitrary)
# 90 = original top edge moves to the LEFT side of the output
# 270 = original top edge moves to the RIGHT side of the output
```

**flip**: Mirror image
```bash
python scripts/image_ops.py flip input.png -d horizontal -o output.png
# -d/--direction: horizontal or vertical
```

**deskew**: Auto-correct small rotation (less than 15 degrees)
```bash
python scripts/image_ops.py deskew input.png -o output.png
# Automatically detects and corrects skew angle
# Note: fills expanded border areas with white. For dark-background images,
# invert first, deskew, then invert back to avoid white border artifacts.
```

**crop**: Extract region
```bash
python scripts/image_ops.py crop input.png --box 100,150,600,400 -o output.png
# --box: left,top,right,bottom (pixels from top-left origin)
```

**scale**: Resize image
```bash
python scripts/image_ops.py scale input.png --factor 2 -o output.png
python scripts/image_ops.py scale input.png --width 800 -o output.png
# --factor: multiplication factor (2 = double size)
# --width/--height: target dimension (maintains aspect ratio if only one specified)
```

### Tonal Operations

**brightness**: Adjust overall brightness
```bash
python scripts/image_ops.py brightness input.png --brightness 1.3 -o output.png
# --brightness: factor (1.0 = unchanged, >1 = brighter, <1 = darker)
```

**contrast**: Adjust overall contrast
```bash
python scripts/image_ops.py contrast input.png --contrast-factor 1.5 -o output.png
# --contrast-factor: factor (1.0 = unchanged, >1 = more contrast)
```

**clahe**: Local contrast enhancement
```bash
python scripts/image_ops.py clahe input.png --clip 2.0 --grid 8 -o output.png
# --clip: contrast limit (1.0-4.0, default 2.0)
# --grid: tile size (default 8)
# Best for: varying lighting, shadows, uneven exposure
```

**histogram**: Global histogram equalization
```bash
python scripts/image_ops.py histogram input.png -o output.png
# Best for: uniformly lit images needing overall contrast boost
# Uses LAB colorspace internally to preserve color fidelity
```

**invert**: Invert colors
```bash
python scripts/image_ops.py invert input.png -o output.png
# Use for: light text on dark background
```

### Detail Operations

**denoise**: Reduce noise
```bash
python scripts/image_ops.py denoise input.png --strength 10 -o output.png
# --strength: 5-20 (default 10). Higher = more smoothing
# Uses bilateral filter (preserves edges but is slow on large images)
# Warning: aggressive denoising destroys fine detail
```

**sharpen**: Enhance edges
```bash
python scripts/image_ops.py sharpen input.png --amount 1.0 --radius 1.0 -o output.png
# --amount: 0.5-2.0 (default 1.0)
# --radius: blur radius (default 1.0)
# Warning: apply only ONCE, after scaling
```

### Specialized Operations

**binarize**: Convert to black and white
```bash
python scripts/image_ops.py binarize input.png --block-size 11 --c 2 -o output.png
# --block-size: neighborhood size for adaptive threshold (odd number, 3-51, default 11)
# --c: constant subtracted from mean (default 2)
# WARNING: Only for high-contrast printed text. Destroys grayscale info.
```

### Utility Operations

**info**: Get image metadata
```bash
python scripts/image_ops.py info input.png
python scripts/image_ops.py info input.png --json
```

**exif**: Fix EXIF orientation
```bash
python scripts/image_ops.py exif input.png -o output.png
# Applies rotation metadata from phone/camera photos
# Harmless to run even if no EXIF data is present
```

## Example Workflow

**Scenario:** User uploads a photo of a whiteboard with meeting notes. Text is small and lighting is uneven.

```
1. ASSESS: Can I read the text? No -- too small and low contrast.

2. DIAGNOSE: Scale problem + quality problem (uneven lighting)

3. PLAN: Crop to content area → Scale up → CLAHE for contrast

4. EXECUTE:
   SESSION_DIR="/tmp/visual_reasoning/session_$(date +%Y%m%d_%H%M%S)"
   mkdir -p "$SESSION_DIR"
   cp input.png "$SESSION_DIR/step_00_original.png"

   "The whiteboard text is small and the lighting is uneven. I'll crop to
   the content area, scale it up, and apply local contrast enhancement."

   python scripts/image_ops.py crop "$SESSION_DIR/step_00_original.png" \
     --box 50,100,800,600 -o "$SESSION_DIR/step_01_cropped.png"
   [VIEW result]

   python scripts/image_ops.py scale "$SESSION_DIR/step_01_cropped.png" \
     --factor 2 -o "$SESSION_DIR/step_02_scaled.png"
   [VIEW result]

   python scripts/image_ops.py clahe "$SESSION_DIR/step_02_scaled.png" \
     --clip 2.0 -o "$SESSION_DIR/step_03_clahe.png"
   [VIEW result]

5. EVALUATE: Text is now readable. Extract information and respond.
```

## Dependencies

The skill requires:
- Python 3.8+
- Pillow (PIL)
- NumPy
- OpenCV (opencv-python-headless)

These are installed automatically on first run if not present. The auto-install uses `pip install --break-system-packages`, which works in the Claude container environment. In other environments, you may need to install these packages manually or use a virtual environment.
