#!/usr/bin/env bash
# setup.sh -- Install dependencies for Qwen 3.5 0.8B inference in the Claude sandbox.
# Must be run once per session (container resets between tasks).
set -euo pipefail

echo "=== Qwen 3.5 0.8B Setup ==="
echo ""

# ── Check available disk space ──────────────────────────────────────────────
DISK_AVAIL_MB=$(df /home/claude --output=avail -BM | tail -1 | tr -d ' M')
echo "Disk available: ${DISK_AVAIL_MB} MB"
if [ "$DISK_AVAIL_MB" -lt 5000 ]; then
    echo "WARNING: Less than 5 GB disk available. Installation may fail."
    echo "Need approximately 5-6 GB for PyTorch (CPU) + transformers + model weights."
    if [ "$DISK_AVAIL_MB" -lt 3000 ]; then
        echo "ERROR: Less than 3 GB available. Aborting to avoid partial install."
        exit 1
    fi
fi

# ── Check available RAM ────────────────────────────────────────────────────
RAM_AVAIL_MB=$(free -m | awk '/Mem:/ {print $7}')
echo "RAM available: ${RAM_AVAIL_MB} MB"
if [ "$RAM_AVAIL_MB" -lt 3000 ]; then
    echo "WARNING: Less than 3 GB RAM available. Model loading may fail or be very slow."
    echo "The model requires approximately 3 GB resident memory at bfloat16."
fi
echo ""

# ── Clear stale caches ────────────────────────────────────────────────────
echo "Clearing stale caches..."
rm -rf /home/claude/.cache/huggingface /home/claude/.cache/pip

# ── Install CPU-only PyTorch ──────────────────────────────────────────────
echo "Installing CPU-only PyTorch..."
pip install torch --index-url https://download.pytorch.org/whl/cpu --break-system-packages -q

# ── Install transformers and accelerate ──────────────────────────────────
echo "Installing transformers and accelerate..."
pip install transformers accelerate --break-system-packages -q

# ── Verify installation ──────────────────────────────────────────────────
echo ""
echo "Verifying installation..."
python3 -c "
import torch
import transformers
print(f'  torch version:        {torch.__version__}')
print(f'  transformers version: {transformers.__version__}')
print(f'  CUDA available:       {torch.cuda.is_available()}')
print(f'  bfloat16 supported:   {torch.is_floating_point(torch.tensor(1.0, dtype=torch.bfloat16))}')
"

# ── Report final disk/RAM state ──────────────────────────────────────────
echo ""
DISK_AFTER_MB=$(df /home/claude --output=avail -BM | tail -1 | tr -d ' M')
RAM_AFTER_MB=$(free -m | awk '/Mem:/ {print $7}')
echo "Post-install disk available: ${DISK_AFTER_MB} MB"
echo "Post-install RAM available:  ${RAM_AFTER_MB} MB"
echo ""
echo "=== Setup complete. Ready to download model and run inference. ==="
