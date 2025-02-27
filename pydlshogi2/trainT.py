import argparse
import logging
import torch
import torch.nn as nn
import torch.optim as optim
from pydlshogi2.network.policy_value_resnet import PolicyValueNetwork
from pydlshogi2.dataloader import HcpeDataLoader
from torchvision.models import resnet18

# 引数設定
parser = argparse.ArgumentParser(description='Train multi-task network')
parser.add_argument('train_data', type=str, nargs='+', help='training data file')
parser.add_argument('test_data', type=str, help='test data file')
parser.add_argument('--gpu', '-g', type=int, default=0, help='GPU ID')
parser.add_argument('--epoch', '-e', type=int, default=1, help='Number of epoch times')
parser.add_argument('--batchsize', '-b', type=int, default=1024, help='Number of positions in each mini-batch')
parser.add_argument('--testbatchsize', type=int, default=1024, help='Number of positions in each test mini-batch')
parser.add_argument('--lr', type=float, default=0.01, help='learning rate')
parser.add_argument('--checkpoint', default='checkpoints/checkpoint-{epoch:03}.pth', help='checkpoint file name')
parser.add_argument('--resume', '-r', default='', help='Resume from snapshot')
parser.add_argument('--eval_interval', type=int, default=100, help='evaluation interval')
parser.add_argument('--log', default=None, help='log file path')
args = parser.parse_args()

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename=args.log,
    level=logging.DEBUG,
)
logging.info('batchsize={}'.format(args.batchsize))
logging.info('lr={}'.format(args.lr))

# デバイス設定
device = torch.device(f"cuda:{args.gpu}" if args.gpu >= 0 else "cpu")

# モデル定義
class MultiTaskNetwork(nn.Module):
    def __init__(self):
        super(MultiTaskNetwork, self).__init__()
        self.resnet = resnet18(weights=None)  # 最新版では `weights=None` が推奨される
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Identity()

        self.policy_head = nn.Linear(num_features, 128)
        self.policy_output = nn.Linear(128, 512)
        self.value_head = nn.Linear(num_features, 128)
        self.value_output = nn.Linear(128, 1)
        self.time_head = nn.Linear(num_features, 1)

    def forward(self, x):
        features = self.resnet(x)
        policy = torch.relu(self.policy_head(features))
        policy = self.policy_output(policy)
        value = torch.relu(self.value_head(features))
        value = torch.tanh(self.value_output(value))
        time_output = self.time_head(features)
        return policy, value, time_output

# モデル初期化
model = MultiTaskNetwork().to(device)

# 損失関数
cross_entropy_loss = torch.nn.CrossEntropyLoss()
bce_with_logits_loss = torch.nn.BCEWithLogitsLoss()
mse_loss = torch.nn.MSELoss()

# オプティマイザ
optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=0.9, weight_decay=0.0001)

# チェックポイント読み込み
if args.resume:
    logging.info(f'Loading the checkpoint from {args.resume}')
    checkpoint = torch.load(args.resume, map_location=device)
    model.load_state_dict(checkpoint['model'])
    optimizer.load_state_dict(checkpoint['optimizer'])

# データローダー設定
train_dataloader = HcpeDataLoader(args.train_data, args.batchsize, device, shuffle=True)
test_dataloader = HcpeDataLoader(args.test_data, args.testbatchsize, device)

# 正解率計算関数
def accuracy(y, t):
    return (torch.max(y, 1)[1] == t).sum().item() / len(t)

def binary_accuracy(y, t):
    pred = y >= 0
    truth = t >= 0.5
    return pred.eq(truth).sum().item() / len(t)

def r2_score(y_pred, y_true):
    ss_res = ((y_true - y_pred) ** 2).sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    return 1 - ss_res / ss_tot

# チェックポイント保存
def save_checkpoint(epoch, t):
    path = args.checkpoint.format(epoch=epoch, step=t)
    logging.info(f'Saving the checkpoint to {path}')
    torch.save({
        'epoch': epoch,
        't': t,
        'model': model.state_dict(),
        'optimizer': optimizer.state_dict(),
    }, path)

# 評価関数
def evaluate_model():
    model.eval()
    total_loss_policy, total_loss_value, total_loss_time = 0, 0, 0
    total_accuracy_policy, total_accuracy_value, total_r2_time = 0, 0, 0
    num_batches = 0

    with torch.no_grad():
        for x, move_label, result, time_label in test_dataloader:
            y1, y2, y3 = model(x)
            loss_policy = cross_entropy_loss(y1, move_label)
            loss_value = bce_with_logits_loss(y2, result)
            loss_time = mse_loss(y3.squeeze(), time_label)

            total_loss_policy += loss_policy.item()
            total_loss_value += loss_value.item()
            total_loss_time += loss_time.item()
            total_accuracy_policy += accuracy(y1, move_label)
            total_accuracy_value += binary_accuracy(y2, result)
            total_r2_time += r2_score(y3.squeeze(), time_label)
            num_batches += 1

    logging.info(f"Test Loss - Policy: {total_loss_policy / num_batches:.4f}, "
                 f"Value: {total_loss_value / num_batches:.4f}, "
                 f"Time: {total_loss_time / num_batches:.4f}")
    logging.info(f"Test Accuracy - Policy: {total_accuracy_policy / num_batches:.4f}, "
                 f"Value: {total_accuracy_value / num_batches:.4f}, "
                 f"R2 Time: {total_r2_time / num_batches:.4f}")

# 学習ループ
t = 0  # トータルステップ数
for epoch in range(1, args.epoch + 1):
    model.train()
    total_loss_policy, total_loss_value, total_loss_time = 0, 0, 0
    num_batches = 0

    for x, move_label, result, time_label in train_dataloader:
        y1, y2, y3 = model(x)
        loss_policy = cross_entropy_loss(y1, move_label)
        loss_value = bce_with_logits_loss(y2, result)
        loss_time = mse_loss(y3.squeeze(), time_label)
        loss = loss_policy + loss_value + loss_time

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss_policy += loss_policy.item()
        total_loss_value += loss_value.item()
        total_loss_time += loss_time.item()
        num_batches += 1
        t += 1

        if t % args.eval_interval == 0:
            logging.info(f"Epoch {epoch}, Step {t} - Train Loss: Policy {total_loss_policy / num_batches:.4f}, "
                         f"Value {total_loss_value / num_batches:.4f}, Time {total_loss_time / num_batches:.4f}")
            evaluate_model()

    save_checkpoint(epoch, t)
    logging.info(f"Epoch {epoch} completed. Train Loss - Policy: {total_loss_policy / num_batches:.4f}, "
                 f"Value: {total_loss_value / num_batches:.4f}, Time: {total_loss_time / num_batches:.4f}")
