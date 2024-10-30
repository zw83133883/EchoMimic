@echo off
setlocal EnableDelayedExpansion

:: 1. Setup your platform
echo Setting up your platform...

:: Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python 3.10 or later.
    pause
    exit /b
)

:: Pip
where pip >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Pip is not installed. Please install Pip.
    pause
    exit /b
)

:: FFMPEG
::where ffmpeg >nul 2>&1
::if %ERRORLEVEL% neq 0 (
::    echo FFMPEG is not installed. Installing FFMPEG...
::    winget install --id Gyan.FFmpeg -e --source winget
::)

:: Check if FFMPEG is installed
where ffmpeg >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo FFMPEG is not installed. Downloading and installing FFMPEG...
    curl -o ffmpeg-release.zip https://ffmpeg.org/releases/ffmpeg-release-full.7z
    
    echo Extracting FFMPEG...
    tar -xf ffmpeg-release.zip -C "C:\ffmpeg" --strip-components=1
    
    echo Adding FFMPEG to system path...
    setx /M PATH "C:\ffmpeg\bin;%PATH%"
    
    echo FFMPEG installed successfully.
) else (
    echo FFMPEG is already installed.
)

:: Visual Studio 2022 Runtimes
echo Installing Visual Studio 2022 Runtimes...
winget install --id Microsoft.VC++2015-2022Redist-x64 -e --source winget

:: 2. Install dependencies
echo Creating a virtual environment...
python -m venv myenv
call myenv\Scripts\activate

echo Installing required Python packages...
pip install --upgrade pip
pip install -r requirements.txt

:: 3. Install CUDA dependencies by default
echo Installing CUDA dependencies...
pip uninstall -y onnxruntime onnxruntime-gpu
pip install onnxruntime-gpu==1.16.3

:: Install PyTorch and CUDA
echo Installing PyTorch with CUDA 11.8...
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

:: 4. Run the application without execution provider
echo Running the application...
python gui.py

pause
