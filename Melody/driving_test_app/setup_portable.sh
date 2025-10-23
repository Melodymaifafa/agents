#!/bin/bash
# Portable setup script - All dependencies in project folder
# 便携式安装脚本 - 所有依赖都在项目文件夹内

echo "============================================================"
echo "🚗 Driving Test Monitor - Portable Setup"
echo "   驾考监控器 - 便携式安装"
echo "============================================================"
echo ""
echo "This will create a self-contained environment in this folder."
echo "这将在此文件夹中创建一个独立的环境。"
echo ""
echo "✅ All dependencies will be installed HERE, not system-wide"
echo "✅ 所有依赖将安装在这里，不影响系统"
echo ""
echo "Location: $(pwd)/venv"
echo "位置: $(pwd)/venv"
echo ""
read -p "Continue? (y/n) / 继续？(y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled / 安装已取消"
    exit 0
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "❌ Python 3 未安装！"
    echo "Please install Python 3.8+ from python.org"
    echo "请从 python.org 安装 Python 3.8+"
    exit 1
fi

echo ""
echo "✓ Python found: $(python3 --version)"

# Create virtual environment in project folder
echo ""
echo "============================================================"
echo "📦 Creating virtual environment / 创建虚拟环境..."
echo "============================================================"

python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    echo "❌ 创建虚拟环境失败"
    exit 1
fi

echo "✓ Virtual environment created / 虚拟环境已创建"

# Activate virtual environment
echo ""
echo "Activating virtual environment / 激活虚拟环境..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip / 升级 pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "============================================================"
echo "📥 Installing dependencies / 安装依赖..."
echo "============================================================"

# Only install playwright and httpx (no gradio needed for tkinter GUI)
pip install playwright>=1.49.1 httpx>=0.28.1

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "❌ 安装依赖失败"
    exit 1
fi

echo ""
echo "✓ Dependencies installed / 依赖已安装"

# Install Playwright browser
echo ""
echo "============================================================"
echo "🌐 Installing Playwright browser / 安装 Playwright 浏览器..."
echo "============================================================"
echo ""
echo "This will download ~200MB to: ./venv/"
echo "这将下载约 200MB 到: ./venv/"
echo ""

# Set Playwright browsers path to venv
export PLAYWRIGHT_BROWSERS_PATH="$PWD/venv/playwright-browsers"
python -m playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Playwright browser"
    echo "❌ 安装 Playwright 浏览器失败"
    exit 1
fi

echo ""
echo "✓ Playwright browser installed / Playwright 浏览器已安装"

# Create activation helper script
echo ""
echo "Creating launcher script / 创建启动脚本..."

cat > start_monitor.sh << 'EOF'
#!/bin/bash
# Launcher script with embedded virtual environment

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup_portable.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set Playwright browsers path
export PLAYWRIGHT_BROWSERS_PATH="$SCRIPT_DIR/venv/playwright-browsers"

# Run the application
echo "Starting Driving Test Monitor / 启动驾考监控器..."
python app_gui.py

# Deactivate when done
deactivate
EOF

chmod +x start_monitor.sh

echo ""
echo "============================================================"
echo "✅ Portable setup complete! / 便携式安装完成！"
echo "============================================================"
echo ""
echo "📂 Everything is installed in: $(pwd)"
echo "📂 所有文件都安装在: $(pwd)"
echo ""
echo "Folder structure / 文件夹结构:"
echo "  venv/                    - Virtual environment / 虚拟环境"
echo "  venv/lib/                - Python packages / Python 包"
echo "  venv/playwright-browsers/- Browser files / 浏览器文件"
echo ""
echo "To run the application / 运行程序:"
echo "  ./start_monitor.sh"
echo ""
echo "To share with friends / 分享给朋友:"
echo "  1. Zip this entire folder / 压缩整个文件夹"
echo "  2. They just run: ./start_monitor.sh"
echo "     他们只需运行: ./start_monitor.sh"
echo ""
echo "To uninstall / 卸载:"
echo "  Simply delete this folder / 直接删除此文件夹即可"
echo ""
echo "============================================================"
