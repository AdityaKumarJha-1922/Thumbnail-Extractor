@echo off
REM ----------------------------------------------
REM Thumbnail Runner - supports drag & drop OR folder picker
REM Saves output to: C:\Users\adity\Pictures\Thumbnails
REM Runs: python "C:\Users\adity\Downloads\thumbnail_extractor_ffmpeg.py"
REM Default image format: png (you can change below)
REM ----------------------------------------------
setlocal enabledelayedexpansion

REM Default python script path in Downloads - CHANGE "adity" TO YOUR USERNAME
set "PY_SCRIPT=C:\Users\adity\Downloads\thumbnail_extractor_ffmpeg.py"

REM If user dragged a folder onto the .bat, %1 will contain it.
if "%~1"=="" (
    REM No argument: open a folder browser dialog (PowerShell) and capture result
    for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command ^
        "Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.FolderBrowserDialog; $f.Description = 'Select the INPUT video folder'; $f.ShowNewFolderButton = $false; if ($f.ShowDialog() -eq 'OK') { Write-Output $f.SelectedPath }"`) do (
        set "INPUT_FOLDER=%%I"
    )
) else (
    REM Use dragged/dropped argument (remove quotes if present)
    set "INPUT_FOLDER=%~1"
)

REM If still empty or user canceled folder picker, exit
if not defined INPUT_FOLDER (
    echo No input folder selected. Exiting...
    pause
    exit /b 1
)

REM Normalize with powershell to remove trailing backslash and spaces
for /f "usebackq delims=" %%N in (`powershell -NoProfile -Command "Write-Output (Resolve-Path -Path '%INPUT_FOLDER%').Path"`) do set "INPUT_FOLDER=%%N"

echo.
echo Selected input folder:
echo     %INPUT_FOLDER%
echo.

REM Set a fixed output directory on Desktop - CHANGE "adity" TO YOUR USERNAME
set "OUTPUT_FOLDER=C:\Users\adity\Desktop\Thumbnails"

REM Create the directory if it doesn't exist
if not exist "%OUTPUT_FOLDER%" mkdir "%OUTPUT_FOLDER%"

REM Set default image format (png). Change to jpeg if you want.
set "IMG_FORMAT=png"

echo Output folder will be:
echo     %OUTPUT_FOLDER%
echo.

REM Run the python script
REM (The python script will create thumbnails for ALL supported video files inside INPUT_FOLDER)
python "%PY_SCRIPT%" "%INPUT_FOLDER%" -o "%OUTPUT_FOLDER%" -f %IMG_FORMAT%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Done! Thumbnails saved to:
    echo     %OUTPUT_FOLDER%
) else (
    echo.
    echo There was an error. Check the messages above.
)

pause
endlocal