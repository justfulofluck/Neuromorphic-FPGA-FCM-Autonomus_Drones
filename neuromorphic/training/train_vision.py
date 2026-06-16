import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
from ..models.vision_snn import VisionSNN
from ..data.dataset import SNNDataset
from .utils import AverageMeter, EarlyStopping, save_checkpoint, plot_training

def train_vision_snn(config):
    device = torch.device('cpu')
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
    train_ds, val_ds, test_ds = random_split(dataset, [train_len, val_len, test_len])

    train_loader = DataLoader(train_ds, batch_size=config['vision_snn']['batch_size'], shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=config['vision_snn']['batch_size'])
    test_loader = DataLoader(test_ds, batch_size=config['vision_snn']['batch_size'])

    H = config['data']['event_resolution'][0]
    model = VisionSNN(
        conv_channels=config['vision_snn']['conv_channels'],
        fc_hidden=config['vision_snn']['fc_hidden'],
        output_dim=config['vision_snn']['output_dim'],
        input_hw=H,
    ).to(device)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config['vision_snn']['lr'],
                                 weight_decay=config['vision_snn']['weight_decay'])
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=config['vision_snn']['lr_factor'],
        patience=config['vision_snn']['lr_patience'], min_lr=1e-6,
    )
    stopper = EarlyStopping(patience=5)

    train_losses, val_losses = [], []

    for epoch in range(config['vision_snn']['epochs']):
        model.train()
        train_loss = AverageMeter()

        for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{config['vision_snn']['epochs']}"):
            events = batch['events'].to(device)
            batch_size = events.size(0)
            events = events.permute(1, 0, 2, 3, 4)
            ego_gt = batch['ego_motion_gt'].to(device)

            ego_pred = model(events)
            loss = criterion(ego_pred, ego_gt)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss.update(loss.item(), batch_size)

        model.eval()
        val_loss = AverageMeter()
        with torch.no_grad():
            for batch in val_loader:
                events = batch['events'].to(device)
                events = events.permute(1, 0, 2, 3, 4)
                ego_gt = batch['ego_motion_gt'].to(device)
                ego_pred = model(events)
                loss = criterion(ego_pred, ego_gt)
                val_loss.update(loss.item(), events.size(0))

        scheduler.step(val_loss.avg)
        train_losses.append(train_loss.avg)
        val_losses.append(val_loss.avg)

        print(f"Epoch {epoch+1}: train_loss={train_loss.avg:.4f}, val_loss={val_loss.avg:.4f}")

        if stopper(val_loss.avg):
            print(f"Early stopping at epoch {epoch+1}")
            break

    save_checkpoint({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'train_loss': train_losses,
        'val_loss': val_losses,
    }, 'checkpoints/vision_snn.pt')

    plot_training(train_losses, val_losses, [], 'checkpoints/vision_training.png')

    model.eval()
    test_loss = AverageMeter()
    with torch.no_grad():
        for batch in test_loader:
            events = batch['events'].to(device)
            events = events.permute(1, 0, 2, 3, 4)
            ego_gt = batch['ego_motion_gt'].to(device)
            ego_pred = model(events)
            loss = criterion(ego_pred, ego_gt)
            test_loss.update(loss.item(), events.size(0))
    print(f"Test loss: {test_loss.avg:.4f}")

    return model
