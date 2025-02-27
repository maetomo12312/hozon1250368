import torch
import os

# モデルの定義（例: ニューラルネットワーク）
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # モデルの層を定義 (適切なモデルに変更する)
        self.fc1 = torch.nn.Linear(512, 256)
        self.fc2 = torch.nn.Linear(256, 128)
        self.fc3 = torch.nn.Linear(128, 10)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 新しいモデルとオプティマイザを初期化
model = Net()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 初期の状態を保存する (学習が始まる前の状態)
checkpoint = {
    'epoch': 0,  # 初期化時なのでエポックは0
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'train_loss': None,  # 損失値の初期化
    'test_loss': None,   # 損失値の初期化
    'train_accuracy': None,  # 精度の初期化
    'test_accuracy': None    # 精度の初期化
}

# 保存先のパスを設定
checkpoint_path = './checkpoints/checkpoint-002.pth'

# ディレクトリが存在しない場合は作成
os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)

# チェックポイントの保存
torch.save(checkpoint, checkpoint_path)

print(f'Initialized checkpoint saved to {checkpoint_path}')
