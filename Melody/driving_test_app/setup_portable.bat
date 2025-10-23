@echo off
REM Portable setup script - All dependencies in project folder
REM 便携式安装脚本 - 所有依赖都在项目文件夹内

echo ============================================================
echo 🚗 Driving Test Monitor - Portable Setup
echo    驾考监控器 - 便携式安装
echo ============================================================
echo.
echo This will create a self-contained environment in this folder.
echo 这将在此文件夹中创建一个独立的环境。
echo.
echo ✅ All dependencies will be installed HERE, not system-wide
echo ✅ 所有依赖将安装在这里，不影响系统
echo.
echo Location: %CD%\venv
echo 位置: %CD%\venv
echo.
set /p confirm="Continue? (y/n) / 继续？(y/n): "
if /i not "%confirm%"=="y" (
    echo Setup cancelled / 安装已取消
    exit /b 0
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo ❌ Python 未安装！
    echo Please install Python 3.8+ from python.org
    echo 请从 python.org 安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo ✓ Python found
python --version

REM Create virtual environment in project folder
echo.
echo ============================================================
echo 📦 Creating virtual environment / 创建虚拟环境...
echo ============================================================

python -m venv venv

if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    echo ❌ 创建虚拟环境失败
    pause
    exit /b 1
)

echo ✓ Virtual environment created / 虚拟环境已创建

REM Activate virtual environment
echo.
echo Activating virtual environment / 激活虚拟环境...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip / 升级 pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo ============================================================
echo 📥 Installing dependencies / 安装依赖...
echo ============================================================

REM Only install playwright and httpx (no gradio needed for tkinter GUI)
pip install playwright>=1.49.1 httpx>=0.28.1

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo ❌ 安装依赖失败
    pause
    exit /b 1
)

echo.
echo ✓ Dependencies installed / 依赖已安装

REM Install Playwright browser
echo.
echo ============================================================
echo 🌐 Installing Playwright browser / 安装 Playwright 浏览器...
echo ============================================================
echo.
echo This will download ~200MB to: .\venv\
echo 这将下载约 200MB 到: .\venv\
echo.

REM Set Playwright browsers path to venv
set PLAYWRIGHT_BROWSERS_PATH=%CD%\venv\playwright-browsers
python -m playwright install chromium

if errorlevel 1 (
    echo ❌ Failed to install Playwright browser
    echo ❌ 安装 Playwright 浏览器失败
    pause
    exit /b 1
)

echo.
echo ✓ Playwright browser installed / Playwright 浏览器已安装

REM Create activation helper script
echo.
echo Creating launcher script / 创建启动脚本...

(
echo @echo off
echo REM Launcher script with embedded virtual environment
echo.
echo REM Get script directory
echo cd /d "%%~dp0"
echo.
echo REM Check if venv exists
echo if not exist "venv" ^(
echo     echo ❌ Virtual environment not found!
echo     echo Please run setup_portable.bat first
echo     pause
echo     exit /b 1
echo ^)
echo.
echo REM Activate virtual environment
echo call venv\Scripts\activate.bat
echo.
echo REM Set Playwright browsers path
echo set PLAYWRIGHT_BROWSERS_PATH=%%CD%%\venv\playwright-browsers
echo.
echo REM Run the application
echo echo Starting Driving Test Monitor / 启动驾考监控器...
echo python app_gui.py
echo.
echo REM Deactivate when done
echo call venv\Scripts\deactivate.bat
echo pause
) > start_monitor.bat

echo.
echo ============================================================
echo ✅ Portable setup complete! / 便携式安装完成！
echo ============================================================
echo.
echo 📂 Everything is installed in: %CD%
echo 📂 所有文件都安装在: %CD%
echo.
echo Folder structure / 文件夹结构:
echo   venv\                    - Virtual environment / 虚拟环境
echo   venv\Lib\                - Python packages / Python 包
echo   venv\playwright-browsers\- Browser files / 浏览器文件
echo.
echo To run the application / 运行程序:
echo   Double-click: start_monitor.bat
echo   双击: start_monitor.bat
echo.
echo To share with friends / 分享给朋友:
echo   1. Zip this entire folder / 压缩整个文件夹
echo   2. They just double-click: start_monitor.bat
echo      他们只需双击: start_monitor.bat
echo.
echo To uninstall / 卸载:
echo   Simply delete this folder / 直接删除此文件夹即可
echo.
echo ============================================================
pause
