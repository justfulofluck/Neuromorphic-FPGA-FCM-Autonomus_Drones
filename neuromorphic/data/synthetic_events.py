import torch

def generate_event_sequence(ego_motion, H=64, W=64, T=10, contrast_threshold=0.03):
    vx, vy, vz = ego_motion[0], ego_motion[1], ego_motion[2]
    wx, wy, wz = ego_motion[3], ego_motion[4], ego_motion[5]

    events = torch.zeros(T, 2, H, W)
    raw = torch.randn(1, 1, H+8, W+8)
    raw = torch.nn.functional.interpolate(raw, size=(H, W), mode='bilinear', align_corners=False)
    intensity = (raw.squeeze() * 0.3).clamp(-1, 1)

    y, x = torch.meshgrid(
        torch.arange(H, dtype=torch.float32) - H / 2,
        torch.arange(W, dtype=torch.float32) - W / 2,
        indexing='ij',
    )

    u = -vx * 2.0 + vz * x * 0.1 + wx * x * y * 0.02 - wy * (1.0 + x ** 2 * 0.02) + wz * y * 0.5
    v = -vy * 2.0 + vz * y * 0.1 + wx * (1.0 + y ** 2 * 0.02) - wy * x * y * 0.02 - wz * x * 0.5

    u = u.clamp(-4, 4)
    v = v.clamp(-4, 4)

    for t in range(T):
        grid_x = (x + u + W / 2) / (W / 2)
        grid_y = (y + v + H / 2) / (H / 2)
        grid = torch.stack([grid_x, grid_y], dim=-1).unsqueeze(0)

        shifted = torch.nn.functional.grid_sample(
            intensity.unsqueeze(0).unsqueeze(0),
            grid, mode='bilinear', align_corners=False,
        ).squeeze()

        diff = shifted - intensity
        events[t, 0] = (diff > contrast_threshold).float()
        events[t, 1] = (diff < -contrast_threshold).float()
        intensity = shifted

    return events

def generate_random_ego_motion():
    v = torch.randn(3) * 0.3
    w = torch.randn(3) * 0.1
    return torch.cat([v, w])
