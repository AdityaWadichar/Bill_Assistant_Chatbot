@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...

    :: Define the Python version and download URL
    set PYTHON_VERSION=3.12.0
    set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
    set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%

    :: Download the Python installer
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%PYTHON_URL%', '%PYTHON_INSTALLER%')"

    :: Install Python silently
    %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

    :: Clean up the installer
    del %PYTHON_INSTALLER%

    echo Python installation completed.
) 

:: Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Installing pip...

    :: Use ensurepip to install pip
    python -m ensurepip --upgrade

    :: Upgrade pip to the latest version
    python -m pip install --upgrade pip

    echo pip installation completed.
) 

:: Check if venv already exists
if not exist venv (
    echo "Creating virtual environment..."
    python -m venv venv
    echo "Virtual environment created!"
    
    echo "Activating virtual environment..."
    call venv\Scripts\activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Dependencies installed!"
) 

:: Activate the virtual environment
call venv\Scripts\activate

:: Run app.py
if exist app.py (
    echo "Running app.py..."
    python app.py
) else (
    echo "app.py not found! Please make sure it exists in the current directory."
    pause
    exit /b
)

pause
