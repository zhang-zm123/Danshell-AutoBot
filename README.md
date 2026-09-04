# 弹壳特工队自动刷主线任务 🎮

基于 Python + OpenCV + ADB 的自动化工具，用于自动刷弹壳特工队主线任务。

## 📋 目录

- [快速开始](#快速开始)
- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [使用方法](#使用方法)
- [配置说明](#配置说明)
- [常见问题](#常见问题)

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/zhang-zm123/Danshell-AutoBot.git
cd Danshell-AutoBot

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 ADB
# 将你的设备连接到电脑并运行：
adb devices

# 4. 运行脚本
python main.py
```

## 📱 环境要求

- **Python 3.8+**
- **安卓设备或模拟器**（已安装弹壳特工队）
- **ADB**（Android Debug Bridge）
- **Windows / macOS / Linux**

## 🔧 安装步骤

### 步骤 1：安装 Python 依赖

```bash
pip install -r requirements.txt
```

依赖包括：
- `opencv-python` - 图像识别
- `pillow` - 图像处理
- `adb-shell` - ADB 控制
- `numpy` - 数据处理

### 步骤 2：安装 ADB

**Windows:**
```bash
# 下载 Android SDK Platform Tools
# https://developer.android.com/studio/releases/platform-tools

# 解压后，将路径添加到环境变量 PATH
# 验证安装
adb version
```

**macOS:**
```bash
brew install android-platform-tools
adb version
```

**Linux:**
```bash
sudo apt-get install android-tools-adb
adb version
```

### 步骤 3：连接安卓设备

**真机连接：**
```bash
# 打开手机开发者模式
# 连接 USB 调试
# 验证连接
adb devices
```

**模拟器连接：**
```bash
# 常见模拟器（自动识别）：
# - 夜神模拟器
# - MuMu 模拟器
# - 网易模拟器
# 自动连接，无需手动配置
adb devices
```

### 步骤 4：配置脚本参数

编辑 `config.json`：

```json
{
  "device_id": "emulator-5554",
  "game_package": "com.danshell.game",
  "screenshot_path": "./screenshots",
  "template_path": "./templates",
  "loop_count": 10,
  "loop_delay": 3,
  "click_delay": 1,
  "debug_mode": true
}
```

## 💻 使用方法

### 基础运行

```bash
# 运行自动刷主线脚本
python main.py
```

### 高级选项

```bash
# 自定义循环次数
python main.py --loop 20

# 调试模式（显示识别过程）
python main.py --debug

# 自定义延迟时间
python main.py --delay 2

# 保存所有截图
python main.py --save-screenshots
```

### 脚本流程

```
1. 连接设备
2. 启动游戏
3. 进入主线任务界面
4. 循环执行：
   - 选择任务
   - 点击开始
   - 等待战斗完成
   - 领取奖励
5. 重复指定次数
6. 断开连接
```

## ⚙️ 配置说明

### config.json 详解

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `device_id` | 设备 ID（adb devices 查看） | `emulator-5554` |
| `game_package` | 游戏包名 | `com.danshell.game` |
| `screenshot_path` | 截图保存路径 | `./screenshots` |
| `template_path` | 模板图片路径 | `./templates` |
| `loop_count` | 循环次数 | `10` |
| `loop_delay` | 循环间隔（秒） | `3` |
| `click_delay` | 点击延迟（秒） | `1` |
| `debug_mode` | 是否开启调试 | `true` |

### 模板文件说明

需要在 `templates/` 目录下放置游戏界面的参考截图：

```
templates/
├── main_scene.png      # 主界面
├── task_list.png       # 任务列表
├── start_button.png    # 开始按钮
├── confirm_button.png  # 确认按钮
├── reward_scene.png    # 奖励界面
└── close_button.png    # 关闭按钮
```

## 🎯 第一次运行指南

1. **启动游戏**
   ```bash
   adb shell am start -n com.danshell.game/.MainActivity
   ```

2. **运行脚本（调试模式）**
   ```bash
   python main.py --debug
   ```

3. **查看截图**
   - 脚本会保存每一步的截图到 `screenshots/` 目录
   - 检查是否正确识别了游戏界面

4. **调整参数**
   - 如果识别不到按钮，在 `main.py` 中调整 `confidence` 阈值
   - 如果点击位置不对，调整 `click_offset`

## ❓ 常见问题

### Q: 连接不上设备怎么办？

```bash
# 重新启动 ADB
adb kill-server
adb start-server
adb devices
```

### Q: 识别不到游戏界面？

1. 确保游戏已启动
2. 检查 `templates/` 目录下的模板图片是否正确
3. 调整 `config.json` 中的 `confidence` 参数（0.7-0.9）
4. 运行 `python debug.py` 查看实时识别情况

### Q: 脚本点击的位置不对？

```bash
# 运行坐标工具
python utils/coordinate_finder.py

# 在弹出的窗口中点击按钮位置，获取准确坐标
# 更新到相应的配置文件中
```

### Q: 游戏崩溃了怎么办？

脚本有自动恢复机制：
```python
# 会自动检测游戏状态
# 如果发现异常，会自动重启游戏
# 可在 config.json 中设置：
"auto_restart": true
```

### Q: 官方会不会封号？

⚠️ **风险声明：**
- 使用自动化脚本有被官方检测到的风险
- **仅建议用小号测试**
- 自己承担所有后果
- 建议交替使用和手动游玩

## 📝 项目结构

```
Danshell-AutoBot/
├── main.py                 # 主程序入口
├── config.json            # 配置文件
├── requirements.txt       # 依赖列表
├── README.md              # 本文件
├── bot/
│   ├── __init__.py
│   ├── auto_bot.py       # 核心自动化逻辑
│   ├── image_utils.py    # 图像识别工具
│   ├── adb_manager.py    # ADB 管理器
│   └── logger.py         # 日志记录
├── templates/            # 游戏界面模板
├── screenshots/          # 截图输出目录
└── utils/
    ├── coordinate_finder.py  # 坐标查找工具
    └── debug.py             # 调试工具
```

## 🔄 工作原理

```
[连接设备] → [启动游戏] → [截屏] → [图像识别] → [模拟点击] → [等待] → [循环]
```

1. **截屏**：通过 ADB 获取当前游戏画面
2. **识别**：使用 OpenCV 模板匹配识别界面元素
3. **点击**：通过 ADB 发送点击指令
4. **等待**：根据游戏响应时间动态延迟
5. **循环**：重复执行直到完成指定次数

## 📚 进阶用法

### 自定义识别策略

编辑 `bot/image_utils.py`：

```python
def find_custom_button(screen, button_name):
    """自定义按钮识别"""
    # 使用 OCR 识别文字
    # 使用特征点识别
    # 使用颜色识别
    pass
```

### 添加新的游戏场景

在 `main.py` 中添加新的处理函数：

```python
def handle_new_scene(bot):
    """处理新场景"""
    screen = bot.take_screenshot()
    # 你的逻辑代码
    pass
```

## 📞 支持和反馈

- 遇到问题？提交 [Issue](https://github.com/zhang-zm123/Danshell-AutoBot/issues)
- 有改进想法？提交 [Pull Request](https://github.com/zhang-zm123/Danshell-AutoBot/pulls)

## ⚖️ 免责声明

本项目仅供学习和研究之用。用户自行承担使用本脚本的所有后果，包括但不限于：
- 游戏账号被封
- 数据丢失
- 其他任何后果

使用前请阅读游戏官方服务条款。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**祝你游戏愉快！** 🎮✨