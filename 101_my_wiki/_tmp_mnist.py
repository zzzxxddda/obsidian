"""
MNIST 数字识别 - PyTorch CNN
训练集: 60,000 张 28x28 灰度手写数字
测试集: 10,000 张
目标: 识别 0-9 十个数字
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# ========== 配置 ==========
BATCH_SIZE = 128
EPOCHS = 10
LEARNING_RATE = 0.001
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"使用设备: {DEVICE}")

# ========== 数据加载 ==========
transform = transforms.Compose([
    transforms.ToTensor(),           # 转为 [0, 1] Tensor
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST 标准化
])

train_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_dataset  = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader  = DataLoader(test_dataset,  batch_size=BATCH_SIZE, shuffle=False)

# ========== 模型定义 (简单 CNN) ==========
class DigitCNN(nn.Module):
    def __init__(self):
        super(DigitCNN, self).__init__()
        self.conv = nn.Sequential(
            # Conv1: 1 -> 32 channels
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),            # 28x28 -> 14x14

            # Conv2: 32 -> 64 channels
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),            # 14x14 -> 7x7
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 10),        # 10 个数字分类
        )

    def forward(self, x):
        return self.fc(self.conv(x))

model = DigitCNN().to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# ========== 训练函数 ==========
def train(epoch):
    model.train()
    total_loss, correct = 0, 0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(DEVICE), target.to(DEVICE)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        correct += (output.argmax(1) == target).sum().item()

        if batch_idx % 100 == 0:
            print(f"  Epoch {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)}]  Loss: {loss.item():.4f}")

    acc = 100. * correct / len(train_loader.dataset)
    avg_loss = total_loss / len(train_loader)
    print(f"训练 epoch {epoch}: Loss={avg_loss:.4f}, Acc={acc:.2f}%")
    return avg_loss, acc

# ========== 测试函数 ==========
def test():
    model.eval()
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(DEVICE), target.to(DEVICE)
            output = model(data)
            correct += (output.argmax(1) == target).sum().item()

    acc = 100. * correct / len(test_loader.dataset)
    print(f"测试集准确率: {acc:.2f}% ({correct}/{len(test_loader.dataset)})")
    return acc

# ========== 主循环 ==========
if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"MNIST 数字识别训练")
    print(f"模型: CNN | Epochs: {EPOCHS} | Batch: {BATCH_SIZE}")
    print(f"{'='*50}\n")

    best_acc = 0
    for epoch in range(1, EPOCHS + 1):
        train(epoch)
        acc = test()
        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), "best_digit_cnn.pth")
            print(f"  → 已保存最优模型: {acc:.2f}%")
        print()

    print(f"\n训练完成！最优准确率: {best_acc:.2f}%")
    print("运行 `python _tmp_mnist.py` 开始训练")
