# 🚗 项目摘要 / Project Summary

## 📂 项目位置 / Project Location

```
/Users/maicuigua/projects/my_projects/agents/Melody/driving_test_app
```

## 📝 文件清单 / File List

```
driving_test_app/
├── app_gui.py                 ✅ GUI 主程序（tkinter）
├── monitor_core.py            ✅ 监控核心逻辑
├── setup_portable.sh          ✅ 便携式安装脚本（Mac/Linux）
├── setup_portable.bat         ✅ 便携式安装脚本（Windows）
├── requirements_portable.txt  ✅ 依赖列表
├── README_PORTABLE.md         ✅ 完整使用指南
├── START_HERE.txt             ✅ 快速开始指南
├── PROJECT_SUMMARY.md         ✅ 本文件
└── .gitignore                 ✅ Git 忽略文件
```

## 🚀 快速开始 / Quick Start

### 步骤 1: 进入项目目录

```bash
cd /Users/maicuigua/projects/my_projects/agents/Melody/driving_test_app
```

### 步骤 2: 运行安装脚本

```bash
./setup_portable.sh
```

这将：
- ✅ 在项目文件夹内创建虚拟环境（`venv/`）
- ✅ 安装 playwright 和 httpx
- ✅ 下载 Chromium 浏览器到 `venv/playwright-browsers/`
- ✅ 生成启动脚本 `start_monitor.sh`

**时间：** 约 2-3 分钟
**大小：** 约 250-300MB（全部在 venv/ 文件夹内）

### 步骤 3: 启动程序

```bash
./start_monitor.sh
```

GUI 窗口会自动打开！

## ✨ 核心特点

| 特点 | 说明 |
|------|------|
| **完全隔离** | 所有依赖在 `venv/` 文件夹，不影响系统 |
| **原生 GUI** | tkinter 界面，无需浏览器 |
| **一键安装** | `setup_portable.sh` 自动处理一切 |
| **双击运行** | `start_monitor.sh` 启动程序 |
| **简单卸载** | 直接删除整个文件夹 |
| **易于分享** | 压缩文件夹即可分享 |

## 📦 安装后的结构

```
driving_test_app/
├── venv/                      ← 虚拟环境（所有依赖）
│   ├── bin/                   ← 可执行文件
│   ├── lib/                   ← Python 包
│   │   └── python3.x/
│   │       └── site-packages/
│   │           ├── playwright/
│   │           └── httpx/
│   └── playwright-browsers/   ← 浏览器文件（~200MB）
│       └── chromium-xxxx/
├── start_monitor.sh           ← 启动脚本（自动生成）
├── app_gui.py                 ← GUI 主程序
└── monitor_core.py            ← 核心逻辑
```

## 🎯 GUI 界面功能

### 标签页 1: 📋 Booking Info / 预订信息
- Booking ID（预订号）
- Family Name（姓氏）
- Preferred Date（首选日期：DD/MM/YYYY）
- Suburb（城市，小写）
- Suburb Dropdown Option（下拉选项，大写）
- Check Interval（检查间隔，秒）

### 标签页 2: 🔔 Notifications / 通知设置
- Pushover User Key（可选）
- Pushover API Token（可选）

### 日志区域
- 实时显示监控进度
- 自动滚动到最新日志

### 控制按钮
- 🚀 Start Monitoring / 开始监控
- ⏹ Stop Monitoring / 停止监控

## 🤝 分享给朋友

### 方法 1: 分享整个文件夹（推荐）

```bash
# 1. 压缩整个文件夹（包括 venv/）
cd /Users/maicuigua/projects/my_projects/agents/Melody/
zip -r driving_test_monitor.zip driving_test_app/

# 2. 发送 driving_test_monitor.zip 给朋友

# 3. 朋友解压后直接运行
#    ./start_monitor.sh (Mac/Linux)
#    双击 start_monitor.bat (Windows)
```

**优点：**
- ✅ 朋友无需安装任何依赖
- ✅ 解压即用
- ✅ 大小：约 250-300MB

### 方法 2: 分享源代码（让朋友自己安装）

```bash
# 1. 只压缩源文件（不包括 venv/）
cd /Users/maicuigua/projects/my_projects/agents/Melody/driving_test_app
zip -r ../driving_test_monitor_source.zip \
    app_gui.py \
    monitor_core.py \
    setup_portable.sh \
    setup_portable.bat \
    requirements_portable.txt \
    README_PORTABLE.md \
    START_HERE.txt

# 2. 发送给朋友

# 3. 朋友运行 setup_portable.sh/bat
```

**优点：**
- ✅ 文件小（约 50KB）
- ✅ 朋友自己下载依赖

## 🗑️ 卸载

超级简单：

```bash
rm -rf /Users/maicuigua/projects/my_projects/agents/Melody/driving_test_app
```

或者直接在 Finder 中删除文件夹。

**就这么简单！** 不会留下任何系统文件。

## 🔍 技术细节

### 依赖
- **playwright** (v1.49.1+) - 浏览器自动化
- **httpx** (v0.28.1+) - HTTP 客户端（Pushover 通知）
- **tkinter** - GUI 框架（Python 标准库）

### Python 版本要求
- Python 3.8 或更高

### 虚拟环境
- 使用 Python 的 `venv` 模块
- 路径：`./venv/`
- 完全独立于系统 Python

### 浏览器
- Chromium（通过 Playwright）
- 路径：`./venv/playwright-browsers/chromium-xxxx/`
- 通过环境变量 `PLAYWRIGHT_BROWSERS_PATH` 指定

## ⚡ 故障排除

### 问题: "venv not found"
**解决：** 重新运行 `./setup_portable.sh`

### 问题: "tkinter not found"
**解决：**
```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk
```

### 问题: "Browser not found"
**解决：**
```bash
source venv/bin/activate
export PLAYWRIGHT_BROWSERS_PATH="$(pwd)/venv/playwright-browsers"
python -m playwright install chromium
```

## 📚 更多信息

- **完整指南：** `README_PORTABLE.md`
- **快速开始：** `START_HERE.txt`
- **中文说明：** 查看上述文档的中文部分

## 🎉 开始使用

```bash
# 1. 进入目录
cd /Users/maicuigua/projects/my_projects/agents/Melody/driving_test_app

# 2. 安装（首次）
./setup_portable.sh

# 3. 运行
./start_monitor.sh

# 4. 填写信息，开始监控！
```

---

**享受便携式体验！** 🚗💨
