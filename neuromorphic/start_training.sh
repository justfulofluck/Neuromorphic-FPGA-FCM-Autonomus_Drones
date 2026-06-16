#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

source venv/bin/activate

echo "+++++++++++++++++++++++++++++++++++++++++++++"
echo "  SNN training Pipeline "
echo "+++++++++++++++++++++++++++++++++++++++++++++"
echo ""

mkdir -p checkpoints

echo "[1/2] Training Vision SNN.."
echo ""
python3 -c "
import sys; sys.path.insert(0, '.')
from neuromorphic.training.train_vision import train_vision_snn
from neuromorphic.config.snn_config import load_config
cfg = load_config()
train_vision_snn(cfg)
"
echo ""
echo "[2/2] training Control SNN..."
echo ""
python3 -c "
import sys; sys.path.insert(0, '.')
from neuromorphic.training.train_control import train_control_snn
from neuromorphic.config.snn_config import load_config
cfg = load_config()
train_control_snn(cfg)
"

echo ""
echo "+++++++++++++++++++++++++++++++++++++++++++"
echo "  Trainning Compleate!"
echo "  Checkpoints saved to: checkpoints/"
echo "+++++++++++++++++++++++++++++++++++++++++++"
echo ""
