import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
from ..models.control_snn import ControlSNN
from ..data.dataset import SNNDataset
from .utils import AverageMeter, EarlyStopping, save_checkpoint, plot_training

def train_control_snn(config):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    dataset = SNNDataset(
        num_samples=config['data']['num_samples'],
        H=config['data']['event_resolution'][0],
        W=config['data']['event_resolution'][1],
        T=config['vision_snn']['time_steps'],
    )
    train_len = int(config['data']['train_split'] * len(dataset))
    val_len = int(config['data']['val_split'] * len(dataset))
    test_len = len(dataset) - train_len - val_len
    train_ds, val_ds, test_ds = random_split(dataset, [train_len, val_len, test_len], generator=torch.Generator().manual_seed(42))

    train_loader = DataLoader(train_ds, batch_size=config['control_snn']['batch_size'], shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=config['control_snn']['batch_size'])
    test_loader = DataLoader(test_ds, batch_size=config['control_snn']['batch_size'])

    T = config['control_snn']['time_steps']
    model = ControlSNN(
        input_dim=config['control_snn']['input_dim'],
        hidden_dims=config['control_snn']['hidden_dims'],
        output_dim=config['control_snn']['output_dim'],
        beta=config['control_snn']['beta'],
        threshold=config['control_snn']['threshold'],
        time_steps=T,
    ).to(device)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config['control_snn']['lr'])
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=config['control_snn']['epochs']
    )
    stopper = EarlyStopping(patience=8)

    train_losses, val_losses, spike_rates = [], [], []

    for epoch in range(config['control_snn']['epochs']):
        model.train()
        train_loss = AverageMeter()
        train_spike = AverageMeter()

        for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{config['control_snn']['epochs']}"):
            ego_motion = batch['ego_motion_gt'].to(device)
            pwm_gt = batch['motor_pwm_gt'].to(device)

            inp = ego_motion.unsqueeze(0).repeat(T, 1, 1)
            spikes = model(inp)
            pwm_pred = model.decode(spikes)
            loss = criterion(pwm_pred, pwm_gt)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss.update(loss.item(), ego_motion.size(0))
            train_spike.update(model.spike_rate(spikes).item(), ego_motion.size(0))

        model.eval()
        val_loss = AverageMeter()
        with torch.no_grad():
            for batch in val_loader:
                ego_motion = batch['ego_motion_gt'].to(device)
                pwm_gt = batch['motor_pwm_gt'].to(device)
                inp = ego_motion.unsqueeze(0).repeat(T, 1, 1)
                spikes = model(inp)
                pwm_pred = model.decode(spikes)
                loss = criterion(pwm_pred, pwm_gt)
                val_loss.update(loss.item(), ego_motion.size(0))

        scheduler.step()
        train_losses.append(train_loss.avg)
        val_losses.append(val_loss.avg)
        spike_rates.append(train_spike.avg)

        print(f"Epoch {epoch+1}: train_loss={train_loss.avg:.4f}, val_loss={val_loss.avg:.4f}, "
              f"spike_rate={train_spike.avg:.4f}")

        stopped = stopper(val_loss.avg)
        if stopper.counter == 0:
            save_checkpoint({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': train_losses,
                'val_loss': val_losses,
            }, 'checkpoints/control_snn_best.pt')

        if stopped:
            print(f"Early stopping at epoch {epoch+1}")
            break

    save_checkpoint({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'train_loss': train_losses,
        'val_loss': val_losses,
    }, 'checkpoints/control_snn.pt')

    plot_training(train_losses, val_losses, spike_rates, 'checkpoints/control_training.png')

    import os
    if os.path.exists('checkpoints/control_snn_best.pt'):
        best_checkpoint = torch.load('checkpoints/control_snn_best.pt', map_location=device)
        model.load_state_dict(best_checkpoint['model_state_dict'])

    model.eval()
    test_loss = AverageMeter()
    with torch.no_grad():
        for batch in test_loader:
            ego_motion = batch['ego_motion_gt'].to(device)
            pwm_gt = batch['motor_pwm_gt'].to(device)
            inp = ego_motion.unsqueeze(0).repeat(T, 1, 1)
            spikes = model(inp)
            pwm_pred = model.decode(spikes)
            loss = criterion(pwm_pred, pwm_gt)
            test_loss.update(loss.item(), ego_motion.size(0))
    print(f"Test loss: {test_loss.avg:.4f}")

    return model
