import torch
import sys
sys.path.append('..')

from models.vision_snn import VisionSNN
from models.control_snn import ControlSNN
from data.synthetic_events import generate_event_sequence, generate_random_ego_motion
from config.snn_config import load_config

def test_full_pipeline(config):
    device = torch.device('cpu')
    print("=" * 50)
    print("End-to-End Hybrid Pipeline Test")
    print("=" * 50)

    viz_cfg = config['vision_snn']
    ctrl_cfg = config['control_snn']
    H, W = config['data']['event_resolution']

    vision_net = VisionSNN(
        conv_channels=viz_cfg['conv_channels'],
        fc_hidden=viz_cfg['fc_hidden'],
        output_dim=viz_cfg['output_dim'],
        input_hw=H,
    ).to(device)

    control_net = ControlSNN(
        input_dim=ctrl_cfg['input_dim'],
        hidden_dims=ctrl_cfg['hidden_dims'],
        output_dim=ctrl_cfg['output_dim'],
        beta=ctrl_cfg['beta'],
        threshold=ctrl_cfg['threshold'],
        time_steps=ctrl_cfg['time_steps'],
    ).to(device)

    ego_motion_gt = generate_random_ego_motion()
    events = generate_event_sequence(ego_motion_gt, H, W, viz_cfg['time_steps']).unsqueeze(1)

    with torch.no_grad():
        ego_pred = vision_net(events)

    ctrl_T = ctrl_cfg['time_steps']
    inp = ego_pred.unsqueeze(0).repeat(ctrl_T, 1, 1)
    with torch.no_grad():
        ctrl_spikes = control_net(inp)
        pwm_pred = control_net.decode(ctrl_spikes)
        control_rate = control_net.spike_rate(ctrl_spikes)

    ego_error = torch.nn.functional.mse_loss(ego_pred, ego_motion_gt)

    print(f"\nEgo-motion GT: {ego_motion_gt.detach().numpy()}")
    print(f"Ego-motion Pred: {ego_pred.detach().numpy()}")
    print(f"Ego-motion MSE: {ego_error.item():.6f}")
    print(f"\nPWM output: {pwm_pred.detach().numpy()}")
    print(f"\nSpike rates - Control: {control_rate.item():.4f}")
    print("\nPipeline test complete!")

if __name__ == '__main__':
    test_full_pipeline()
