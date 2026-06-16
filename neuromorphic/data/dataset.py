import torch
from torch.utils.data import Dataset
from .synthetic_events import generate_event_sequence, generate_random_ego_motion

class SNNDataset(Dataset):
    def __init__(self, num_samples=5000, H=64, W=64, T=10, seed=42):
        super().__init__()
        torch.manual_seed(seed)
        self.events = []
        self.ego_motions = []
        self.pwms = []
        for _ in range(num_samples):
            ego = generate_random_ego_motion()
            ev = generate_event_sequence(ego, H, W, T)
            pwm = (ego[:4] * 0.3 + 0.5 + torch.randn(4) * 0.1).clamp(0, 1)
            self.events.append(ev)
            self.ego_motions.append(ego)
            self.pwms.append(pwm)

    def __len__(self):
        return len(self.events)

    def __getitem__(self, idx):
        return {
            'events': self.events[idx],
            'ego_motion_gt': self.ego_motions[idx],
            'motor_pwm_gt': self.pwms[idx],
        }
