# 🚗 Driving Test Monitor - Portable Version

## 便携式版本 / Portable Version

**完全独立，不影响您的系统！**

**Completely self-contained, won't mess up your system!**

---

## ✨ 主要特点 / Key Features

✅ **所有依赖都在项目文件夹内** / All dependencies in project folder
✅ **不影响系统 Python 环境** / Doesn't affect system Python
✅ **原生 GUI 界面（tkinter）** / Native GUI interface (tkinter)
✅ **双击启动，无需命令行** / Double-click to run, no terminal needed
✅ **完全便携，可以直接分享** / Fully portable, can share directly
✅ **删除文件夹即可卸载** / Uninstall by deleting folder

---

## 📋 系统要求 / Requirements

- **Python 3.8+** (系统自带或从 python.org 下载)
- **200MB 磁盘空间** (用于虚拟环境和浏览器)
- **互联网连接** (首次安装和运行时)

---

## 🚀 安装步骤 / Installation Steps

### macOS/Linux

```bash
# 1. 进入项目文件夹
cd driving_test_app

# 2. 运行便携式安装脚本
chmod +x setup_portable.sh
./setup_portable.sh

# 3. 等待安装完成（约2-3分钟）
# 所有文件都会下载到 ./venv/ 文件夹
```

### Windows

```
1. 双击: setup_portable.bat
2. 等待安装完成（约2-3分钟）
   所有文件都会下载到 .\venv\ 文件夹
```

---

## 🎯 运行程序 / Run the Application

### macOS/Linux

```bash
./start_monitor.sh
```

或者双击 `start_monitor.sh`

### Windows

```
双击: start_monitor.bat
```

---

## 📂 文件夹结构 / Folder Structure

安装完成后的文件夹结构：

```
driving_test_app/
├── venv/                          # 虚拟环境（所有依赖在这里）
│   ├── bin/                       # 可执行文件
│   ├── lib/                       # Python 包
│   │   └── python3.x/
│   │       └── site-packages/
│   │           ├── playwright/    # Playwright 包
│   │           └── httpx/         # HTTPX 包
│   └── playwright-browsers/       # 浏览器文件（~200MB）
│       └── chromium-xxxx/
├── app_gui.py                     # GUI 主程序
├── monitor_core.py                # 监控核心逻辑
├── setup_portable.sh/bat          # 安装脚本
├── start_monitor.sh/bat           # 启动脚本
└── README_PORTABLE.md             # 本文档
```

**重要：** 所有依赖都在 `venv/` 文件夹中，与系统完全隔离！

---

## 💡 使用说明 / How to Use

### 1. 启动程序 / Start Application

双击 `start_monitor.sh` (Mac/Linux) 或 `start_monitor.bat` (Windows)

### 2. 填写信息 / Fill Information

在 GUI 界面的两个标签页中填写：

**📋 Booking Info / 预订信息**
- Booking ID（预订号）
- Family Name（姓氏）
- Preferred Date（首选日期，格式：DD/MM/YYYY）
- Suburb（城市，小写）
- Suburb Dropdown Option（下拉选项，通常大写）
- Check Interval（检查间隔，推荐 5 秒）

**🔔 Notifications / 通知（可选）**
- Pushover User Key
- Pushover API Token

### 3. 开始监控 / Start Monitoring

点击 **"🚀 Start Monitoring"** 按钮

### 4. 查看日志 / View Logs

在下方的日志区域查看实时进度

### 5. 找到时间段 / When Slots Found

- 收到通知（如果设置了 Pushover）
- 浏览器保持打开在预订页面
- 可以立即预订！

### 6. 停止监控 / Stop Monitoring

点击 **"⏹ Stop Monitoring"** 按钮

---

## 🤝 分享给朋友 / Share with Friends

### 方法1：分享整个文件夹（推荐）

1. **压缩文件夹**
   ```bash
   # 先删除一些不需要的文件
   rm -rf __pycache__ .DS_Store

   # 然后压缩
   zip -r driving_test_monitor.zip driving_test_app/
   ```

2. **发送给朋友**
   - 朋友解压后直接双击 `start_monitor.sh` 或 `start_monitor.bat`
   - 不需要安装任何东西！

3. **文件大小**
   - 约 250-300MB（包含所有依赖和浏览器）

### 方法2：让朋友自己安装

1. 只分享项目源文件（不包括 venv/）
2. 朋友运行 `setup_portable.sh` 或 `setup_portable.bat`
3. 依赖会自动下载到他们的文件夹中

---

## 🗑️ 卸载 / Uninstall

**超级简单！**

```bash
# 直接删除整个文件夹
rm -rf driving_test_app/
```

或者：
- **macOS/Linux:** 把文件夹拖到废纸篓
- **Windows:** 删除文件夹

**就这么简单！** 不会留下任何系统文件或注册表项。

---

## 🔍 技术细节 / Technical Details

### 虚拟环境 / Virtual Environment

- 使用 Python 的 `venv` 模块
- 所有包安装在 `./venv/lib/` 中
- 完全独立于系统 Python

### 浏览器隔离 / Browser Isolation

- Playwright 浏览器安装在 `./venv/playwright-browsers/`
- 通过环境变量 `PLAYWRIGHT_BROWSERS_PATH` 指定路径
- 不会安装到系统目录

### GUI 框架 / GUI Framework

- 使用 **tkinter**（Python 标准库）
- 无需额外安装
- 原生界面，启动快速

### 依赖最小化 / Minimal Dependencies

只需要两个外部包：
- **playwright** - 浏览器自动化
- **httpx** - HTTP 客户端（用于 Pushover 通知）

---

## ⚠️ 常见问题 / FAQ

### Q: 会不会影响我电脑上的其他 Python 项目？
A: **不会！** 所有依赖都在 `venv/` 文件夹中，完全隔离。

### Q: 删除文件夹后会留下什么吗？
A: **不会！** 删除文件夹就彻底删除了，没有任何残留。

### Q: 可以移动文件夹位置吗？
A: **可以！** 整个文件夹是便携的，可以移动到任何位置。

### Q: 文件夹有多大？
A: 约 **250-300MB**，包含：
- Python 虚拟环境 (~50MB)
- Playwright 包 (~30MB)
- Chromium 浏览器 (~200MB)

### Q: 需要管理员权限吗？
A: **不需要！** 所有操作都在用户目录中。

### Q: 可以在 U 盘上运行吗？
A: **可以！** 复制整个文件夹到 U 盘，直接运行。

### Q: Python 版本有要求吗？
A: **需要 Python 3.8+**。但虚拟环境会使用系统 Python 的版本。

---

## 🔧 故障排除 / Troubleshooting

### 问题: "venv not found"

**解决方案:**
```bash
# 重新运行安装脚本
./setup_portable.sh    # macOS/Linux
setup_portable.bat     # Windows
```

### 问题: GUI 界面无法打开

**原因:** 可能是 tkinter 未安装

**解决方案:**

**macOS:**
```bash
# 通常 Python 3 自带 tkinter，如果没有：
brew install python-tk
```

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Windows:**
- 重新安装 Python，确保勾选 "tcl/tk and IDLE"

### 问题: 浏览器无法启动

**解决方案:**
```bash
# 重新安装浏览器
source venv/bin/activate  # macOS/Linux
call venv\Scripts\activate.bat  # Windows

export PLAYWRIGHT_BROWSERS_PATH="$(pwd)/venv/playwright-browsers"  # macOS/Linux
set PLAYWRIGHT_BROWSERS_PATH=%CD%\venv\playwright-browsers  # Windows

python -m playwright install chromium
```

---

## 🎉 优势对比 / Comparison

| 特性 | 便携式版本 | 系统安装版本 |
|------|----------|-------------|
| 影响系统 | ❌ 不影响 | ✅ 会影响 |
| 卸载方式 | 删除文件夹 | 需要卸载包 |
| 分享给朋友 | 直接压缩 | 需要重新安装 |
| 多版本共存 | ✅ 支持 | ❌ 不支持 |
| 磁盘空间 | ~300MB | ~300MB |
| 安装速度 | 2-3 分钟 | 2-3 分钟 |

---

## 📝 启动脚本说明 / Launcher Script Details

`start_monitor.sh` / `start_monitor.bat` 会自动：

1. ✅ 检查虚拟环境是否存在
2. ✅ 激活虚拟环境
3. ✅ 设置浏览器路径环境变量
4. ✅ 启动 GUI 应用
5. ✅ 退出时自动清理

**完全自动化！**

---

## 🌟 最佳实践 / Best Practices

### 1. 首次使用

```bash
# 完整流程
./setup_portable.sh     # 安装（只需一次）
./start_monitor.sh      # 启动程序
```

### 2. 日常使用

```bash
./start_monitor.sh      # 直接启动，无需其他操作
```

### 3. 分享给朋友

```bash
# 打包整个文件夹
zip -r monitor.zip driving_test_app/
# 发送 monitor.zip
# 朋友解压后双击 start_monitor.sh/bat
```

### 4. 彻底卸载

```bash
# 直接删除
rm -rf driving_test_app/
# 完成！
```

---

## 📊 文件清单 / File Checklist

安装后应该有这些文件：

```
✅ venv/                     - 虚拟环境
✅ venv/playwright-browsers/ - 浏览器
✅ app_gui.py               - GUI 程序
✅ monitor_core.py          - 核心逻辑
✅ start_monitor.sh/bat     - 启动脚本
✅ setup_portable.sh/bat    - 安装脚本
✅ README_PORTABLE.md       - 本文档
```

---

## 🎯 总结 / Summary

### 为什么选择便携式版本？

✅ **完全隔离** - 不会"弄乱"您的电脑
✅ **易于分享** - 压缩文件夹即可
✅ **简单卸载** - 删除文件夹即可
✅ **多版本共存** - 可以有多个副本
✅ **原生 GUI** - 启动快速，界面友好

### 快速开始

```bash
# 1. 安装（一次）
./setup_portable.sh

# 2. 启动（每次）
./start_monitor.sh

# 3. 卸载（如需）
rm -rf driving_test_app/
```

---

## 🆘 需要帮助？ / Need Help?

1. 查看本文档的故障排除部分
2. 检查 `venv/` 文件夹是否存在
3. 确保 Python 3.8+ 已安装
4. 尝试重新运行 `setup_portable.sh/bat`

---

**享受无忧的便携式体验！** 🎉

**Enjoy the hassle-free portable experience!** 🎉
