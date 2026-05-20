# Visual Reasoning Quick Reference

Condensed command reference. For rationale and detailed guidance, see SKILL.md. For parameter tuning, see `parameters.md`.

## Decision Tree

```
Can I extract the information now?
├── YES → Respond directly
├── PARTIALLY → Read full image first for context, then crop+enhance
│   only the unreadable regions (two-pass pattern)
└── NO → What's the problem?
    ├── Wrong orientation → rotate / flip / deskew
    ├── Too small → crop + scale
    ├── Low contrast → clahe (varied lighting) or contrast (uniform lighting)
    ├── Too dark/bright → brightness
    ├── Noisy → denoise
    ├── Blurry → sharpen (light touch, once only)
    └── Light-on-dark → invert first, then enhance
```

## Operation Order

```
0. exif  →  1. rotate/flip/deskew  →  2. crop/scale  →  3. invert
→  4. brightness/contrast/clahe  →  5. denoise/sharpen  →  6. binarize
```

## Commands

All commands use `python scripts/image_ops.py`. The `-o` flag specifies the output path.

```bash
# Setup
SESSION_DIR="/tmp/visual_reasoning/session_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SESSION_DIR"

# Info
python scripts/image_ops.py info img.png
python scripts/image_ops.py info img.png --json

# EXIF fix
python scripts/image_ops.py exif img.png -o out.png

# Rotate (degrees counter-clockwise; 90 = top goes to LEFT)
python scripts/image_ops.py rotate img.png -a 90 -o out.png
python scripts/image_ops.py rotate img.png -a 180 -o out.png
python scripts/image_ops.py rotate img.png -a 270 -o out.png

# Flip
python scripts/image_ops.py flip img.png -d horizontal -o out.png

# Deskew (auto-detect, < 15 deg; fills borders with white)
python scripts/image_ops.py deskew img.png -o out.png

# Crop (left,top,right,bottom from top-left origin)
python scripts/image_ops.py crop img.png --box 100,100,500,400 -o out.png

# Scale
python scripts/image_ops.py scale img.png --factor 2 -o out.png
python scripts/image_ops.py scale img.png --width 800 -o out.png

# Brightness (1.0 = unchanged)
python scripts/image_ops.py brightness img.png --brightness 1.3 -o out.png

# Contrast (1.0 = unchanged)
python scripts/image_ops.py contrast img.png --contrast-factor 1.5 -o out.png

# CLAHE (local contrast; best for uneven lighting)
python scripts/image_ops.py clahe img.png --clip 2.0 --grid 8 -o out.png

# Histogram equalization (global; uniform lighting only)
python scripts/image_ops.py histogram img.png -o out.png

# Invert (light-on-dark to dark-on-light)
python scripts/image_ops.py invert img.png -o out.png

# Denoise (strength 5-20; slow on large images)
python scripts/image_ops.py denoise img.png --strength 10 -o out.png

# Sharpen (apply ONCE, AFTER scaling)
python scripts/image_ops.py sharpen img.png --amount 1.0 --radius 1.0 -o out.png

# Binarize (printed text ONLY; block-size must be odd, 3-51)
python scripts/image_ops.py binarize img.png --block-size 11 --c 2 -o out.png

# Auto-named session output
python scripts/image_ops.py rotate img.png -a 90 --session "$SESSION_DIR"
```

## Task Recipes

| Task | Recipe |
|------|--------|
| OCR text | deskew → scale (target 30-50px chars) → clahe → (binarize) |
| Whiteboard | crop → clahe → light sharpen |
| Diagram | rotate → crop → contrast |
| Small detail | crop tight → scale 2-4x → sharpen |
| Dark photo | exif → clahe |
| Doc in photo | exif → crop to doc edges → assess → crop sub-regions → enhance |

## Key Thresholds

- **1568px**: Images with long edge above this are downscaled before the model sees them. Crop first for best detail.
- **200px**: Images below this on any edge degrade model performance. Scale up first.
- **4000px**: Above this, `denoise` becomes very slow. Crop or use CLAHE/contrast instead.

## Stop Conditions

Stop after: success, 2 consecutive no-improvement ops, quality degradation, 3 failed alternative sequences for same problem, or 5 total operations.
