#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

source venv/bin/activate

echo "========================================"
echo "  Hybrid SNN Trained Model Test"
echo "========================================"
echo ""

if [ ! -f "checkpoints/vision_snn.pt" ]; then
  echo " vision_snn.pt not found! Train first."
  exit 1
fi
if [ ! -f "checkpoints/control_snn.pt" ]; then
  echo " control_snn.pt not found! Train first."
  exit 1
fi

echo " Vision checkpoint found"
echo " Control checkpoint found"
echo ""

python3 -c "
import sys; sys.path.insert(0, '.')
import torch
from neuromorphic.models.vision_snn import VisionSNN
from neuromorphic.models.control_snn import ControlSNN
from neuromorphic.data.synthetic_events import generate_event_sequence, generate_random_ego_motion
from neuromorphic.config.snn_config import load_config

cfg = load_config()
H, W = cfg['data']['event_resolution']
Tv = cfg['vision_snn']['time_steps']
Tc = cfg['control_snn']['time_steps']

vision = VisionSNN(
    conv_channels=cfg['vision_snn']['conv_channels'],
    fc_hidden=cfg['vision_snn']['fc_hidden'],
    output_dim=cfg['vision_snn']['output_dim'],
    input_hw=H,
)
vision.load_state_dict(torch.load('checkpoints/vision_snn.pt', map_location='cpu')['model_state_dict'])
vision.eval()
print(f' Vision CNN loaded ({sum(p.numel() for p in vision.parameters()):,} params)')

control = ControlSNN(
    input_dim=cfg['control_snn']['input_dim'],
    hidden_dims=cfg['control_snn']['hidden_dims'],
    output_dim=cfg['control_snn']['output_dim'],
    beta=cfg['control_snn']['beta'],
    threshold=cfg['control_snn']['threshold'],
    time_steps=Tc,
)
control.load_state_dict(torch.load('checkpoints/control_snn.pt', map_location='cpu')['model_state_dict'])
control.eval()
print(f' Control SNN loaded ({sum(p.numel() for p in control.parameters()):,} params)')
print()

ego_gt = generate_random_ego_motion()
events = generate_event_sequence(ego_gt, H, W, Tv).unsqueeze(1)

with torch.no_grad():
    ego_pred = vision(events)
    vr = torch.tensor(0.0)
    inp = ego_pred.unsqueeze(0).repeat(Tc, 1, 1)
    cs = control(inp)
    pwm = control.decode(cs)
    cr = control.spike_rate(cs)

mse = torch.nn.functional.mse_loss(ego_pred.squeeze(0), ego_gt)
print(f'Ego-motion GT:     {ego_gt.numpy()}')
print(f'Ego-motion Pred:   {ego_pred.squeeze().numpy()}')
print(f'Ego-motion MSE:    {mse.item():.4f}')
print(f'Control spike rate: {cr.item():.4f}')
print(f'PWM output:         {pwm.squeeze().tolist()}')
"

echo ""
echo "========================================"
echo "  Test Complete!"
echo "========================================"
