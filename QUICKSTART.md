#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速开始指南 - 弹壳特工队自动刷主线任务
一步步教你如何运行这个项目
"""

# ============================================================================
# 📱 【第一步】连接设备并验证 ADB
# ============================================================================

"""
1.1 连接安卓设备到电脑

【真机连接】
- 打开手机「设置」→ 「关于手机」
- 找到「版本号」，连续点击 7 次
- 返回设置，打开「开发者选项」
- 启用「USB 调试」
- 用 USB 数据线连接到电脑
- 手机会提示授权，点击「允许」

【模拟器连接】
- 启动夜神、MuMu 等模拟器
- 自动连接，无需手动配置

1.2 验证 ADB 连接
在电脑终端/命令行运行：

    adb devices

输出示例（✅ 说明连接成功）：
    List of attached devices
    emulator-5554          device
    或
    192.168.1.100:5555    device

❌ 如果看不���设备，检查：
  - USB 数据线是否连接
  - 手机是否启用了 USB 调试
  - ADB 是否正确安装
"""

# ============================================================================
# 📂 【第二步】下载项目代码
# ============================================================================

"""
2.1 克隆项目到本地

在电脑终端/命令行运行：

    git clone https://github.com/zhang-zm123/Danshell-AutoBot.git
    cd Danshell-AutoBot

2.2 项目结构说明
    
    Danshell-AutoBot/
    ├── main.py                 # ← 主程序（运行这个）
    ├── config.json            # ← 配置文件（需要修改）
    ├── requirements.txt       # ← Python 依赖
    ├── README.md              # 详细说明
    ├── bot/                   # 核心模块
    │   ├── auto_bot.py       # 自动化逻辑
    │   ├── adb_manager.py    # ADB 控制
    │   ├── image_utils.py    # 图像识别
    │   └── logger.py         # 日志记录
    ├── templates/            # ⭐ 游戏界面模板（需要添加）
    ├── screenshots/          # 运行时截图输出
    └── utils/
        ├── debug.py         # 调试工具
        └── coordinate_finder.py  # 坐标查找工具
"""

# ============================================================================
# 🐍 【第三步】安装 Python 依赖
# ============================================================================

"""
3.1 安装依赖包

在项目目录运行：

    pip install -r requirements.txt

等待安装完成（会看到很多输出）

❌ 如果遇到错误：
  - 确保 Python 版本 >= 3.8（运行 python --version 检查）
  - 尝试用 pip3：pip3 install -r requirements.txt
  - 可能需要管理员权限（Windows 用管理员打开 CMD）
"""

# ============================================================================
# ⚙️ 【第四步】修改配置文件
# ============================================================================

"""
4.1 编辑 config.json

用任何文本编辑器打开 config.json，修改以下内容：

【修改前】：
{
  "device_id": "emulator-5554",    ← 改这里！
  "game_package": "com.danshell.game",
  ...
}

【修改后】：
{
  "device_id": "你的设备ID",        ← 改成从 adb devices 看到的 ID
  "game_package": "com.danshell.game",
  "loop_count": 10,                 ← 循环次数
  "loop_delay": 3,                  ← 轮次间隔（秒）
  "click_delay": 1,                 ← 点击延迟（秒）
  "debug_mode": true                ← 调试模式（建议开启）
}

例如，如果 adb devices 显示：
    emulator-5554          device
    192.168.1.100:5555    device

则 device_id 可以是 "emulator-5554" 或 "192.168.1.100:5555"
"""

# ============================================================================
# 📸 【第五步】准备游戏界面模板（最重要！）
# ============================================================================

"""
⭐ 这一步最关键！脚本需要游戏截图来识别按钮位置

【方法 1】使用坐标工具（推荐、最简单）

1. 在手机上启动弹壳特工队游戏
2. 在电脑终端运行：
    
    python utils/coordinate_finder.py

3. 会弹出手机当前屏幕的截图窗口
4. 在窗口中点击各个游戏按钮的位置：
   - 点击「主线」按钮
   - 点击「开始战斗」按钮
   - 点击「领取奖励」按钮
   等等...

5. 按 ESC 键退出
6. 坐标会自动保存到 coordinates.json

【方法 2】手动截屏（如果方法1不行）

1. 用以下命令截屏：
    
    adb shell screencap -p /sdcard/screen.png
    adb pull /sdcard/screen.png

2. 用图片编辑器打开 screen.png（Windows 画图、Mac 预览、Linux GIMP 等）

3. 截取各个按钮的局部图片，保存到 templates/ 文件夹：
   - templates/main_line_button.png    (主线按钮)
   - templates/select_task.png         (选择任务)
   - templates/start_battle.png        (开始战斗)
   - templates/battle_result.png       (战斗完成提示)
   - templates/claim_reward.png        (领取奖励)
   - templates/back_button.png         (返回按钮)

4. 确保裁剪的图片只包含按钮本身，周围留一点空白

【检查】：

    templates/ 目录下应该有：
    ✅ main_line_button.png
    ✅ select_task.png
    ✅ start_battle.png
    ✅ battle_result.png
    ✅ claim_reward.png
    ✅ back_button.png
"""

# ============================================================================
# 🚀 【第六步】运行脚本
# ============================================================================

"""
【第一次运行 - 调试模式（推荐）】

在项目目录运行：

    python main.py --debug

输出示例：
    ==================================================
    🎮 弹壳特工队自动刷主线任务启动
    ==================================================
    🔍 检查运行环境...
    ✅ ADB 检查通过
    ✅ 设备已连接: emulator-5554
    📋 配置信息:
       - 循环次数: 10
       - 循环延迟: 3s
       - 点击延迟: 1s
       - 调试模式: 开启
    
    📱 启动游戏...
    ✅ 游戏已启动
    ⏳ 等待游戏加载...
    
    🎯 开始自动化运行...
    【第 1/10 轮】
    🎮 开始第 1 轮自动化
    👆 点击: (540, 1200)
    ✅ 找到按钮 start_battle.png: (540, 1200), 置信度: 0.95
    ...

【自定义参数运行】

    # 运行 20 轮
    python main.py --loop 20

    # 增加延迟时间
    python main.py --delay 5

    # 组合参数
    python main.py --loop 15 --debug --delay 2

【正式运行（后台）】

    python main.py

    # 或运行指定次数
    python main.py --loop 50
"""

# ============================================================================
# 🔍 【故障排查】
# ============================================================================

"""
【问题 1】ADB 找不到设备

❌ 运行 adb devices 没有看到设备

解决步骤：
1. 检查 USB 数据线是否插好
2. 重新启用手机的 USB 调试
3. 重启 ADB 服务：
   adb kill-server
   adb start-server
4. 再次运行 adb devices

【问题 2】识别不到按钮

❌ 脚本找不到游戏中的按钮

解决步骤：
1. 确保 templates/ 目录下有游戏截图
2. 调整 config.json 中的 confidence 值（改小一点）：
   "confidence": 0.7  (从 0.8 改成 0.7)
3. 运行调试模式查看截图：
   python main.py --debug
4. 查看 screenshots/ 中的截图是否正确

【问题 3】游戏崩溃或卡死

❌ 游戏在运行中崩溃了

解决步骤：
1. 脚本会自动尝试重启游戏（如果配置了 auto_restart）
2. 如果还是失败，手动停止脚本（Ctrl+C）
3. 手动重启游戏：
   adb shell am start -n com.danshell.game/.MainActivity
4. 重新运行脚本

【问题 4】Python 版本错误

❌ ModuleNotFoundError 或其他导入错误

解决步骤：
1. 检查 Python 版本：
   python --version
2. 确保 >= 3.8，否则升级 Python
3. 重新安装依赖：
   pip install --upgrade -r requirements.txt

【问题 5】找不到 config.json

❌ FileNotFoundError: config.json

解决步骤：
1. 确保在项目根目录运行（Danshell-AutoBot/ 文件夹里）
2. 用 cd 命令进入项目文件夹：
   cd path/to/Danshell-AutoBot
3. 验证 config.json 存在：
   ls config.json  (Linux/Mac)
   dir config.json (Windows)
"""

# ============================================================================
# 📊 【运行流程图】
# ============================================================================

"""
【完整执行流程】

    开始
      ↓
    ✅ 连接设备 (adb devices)
      ↓
    ✅ 启动游戏
      ↓
    ✅ 进入主线任务界面
      ↓
    【循环开始】
      ↓
    📸 截屏
      ↓
    🔍 识别游戏界面
      ↓
    👆 点击「开始战斗」
      ↓
    ⏳ 等待战斗完成 (60秒超时)
      ↓
    👆 点击「领取奖励」
      ↓
    👆 点击「返回」
      ↓
    【循环结束】 × 指定次数
      ↓
    ✅ 完成！显示统计信息
      ↓
    结束
"""

# ============================================================================
# 💡 【常用命令速查】
# ============================================================================

"""
【基础命令】

# 检查 ADB 连接
adb devices

# 启动游戏
adb shell am start -n com.danshell.game/.MainActivity

# 杀死游戏进程
adb shell am force-stop com.danshell.game

# 截屏
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png

【脚本命令】

# 调试运行（推荐）
python main.py --debug

# 正常运行
python main.py

# 运行指定次数
python main.py --loop 20

# 自定义延迟
python main.py --delay 5

# 运行坐标工具
python utils/coordinate_finder.py

# 运行调试工具（每 3 秒截屏一次）
python utils/debug.py

【停止脚本】

按 Ctrl+C 中断程序运行
"""

# ============================================================================
# ✅ 【检查清单】
# ============================================================================

"""
运行前请检查以下项目：

□ 已安装 Python 3.8+
□ 已安装 ADB
□ 手机/模拟器已连接（adb devices 能看到）
□ 已安装弹壳特工队游戏
□ 已修改 config.json 中的 device_id
□ 已在 templates/ 文件夹中放入游戏截图
□ 已运行 pip install -r requirements.txt

如果全部打勾，就可以运行了！🚀
"""

# ============================================================================
# 🎮 【现在就开始！】
# ============================================================================

print("""
╔═══════════════════════════════════════════════════════════════╗
║     弹壳特工队自动刷主线任务 - 快速开始指南                    ║
║                  Danshell AutoBot                             ║
╚═══════════════════════════════════════════════════════════════╝

📍 项目地址：https://github.com/zhang-zm123/Danshell-AutoBot

【快速启动（3 步）】

1️⃣ 安装依赖
   pip install -r requirements.txt

2️⃣ 修改配置
   编辑 config.json，改 device_id 为你的设备 ID

3️⃣ 运行脚本
   python main.py --debug

【详细步骤见本文件中的文档】

有问题？按照文件中的「【故障排查】」部分查找答案。

祝你使用愉快！🎉
""")

if __name__ == "__main__":
    print(__doc__)
