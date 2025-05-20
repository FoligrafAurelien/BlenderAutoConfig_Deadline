@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

:: Detect current folder name (e.g., "Blender 4.2")
for %%A in ("%cd%") do set "FolderName=%%~nxA"

:: Optional: print detected folder
:: echo Current folder: %FolderName%

:: Path to .env file
set "ENV_FILE=..\config.env"
set "ENV_STATE=PROD"

:: Read config.env if present
if exist "%ENV_FILE%" (
    for /f "usebackq tokens=1,2 delims== " %%A in ("%ENV_FILE%") do (
        if /I "%%A"=="STATE" (
            set "ENV_STATE=%%B"
        )
    )
) else (
    echo [INFO] config.env not found, defaulting to PROD mode.
)

:: Remove potential spaces
set "ENV_STATE=%ENV_STATE: =%"

:: Dynamic config path
set "CONFIG_BASE=\\SRVDEADLINE\DeadlineRepository10\custom\Blender"
set "CONFIG_PATH=%CONFIG_BASE%\%FolderName%"

:: Check if CONFIG_PATH exists
if not exist "%CONFIG_PATH%" (
    echo [INFO] %CONFIG_PATH% does not exist, creating it...

    if exist "%CONFIG_BASE%\BlenderBase" (
        xcopy /E /I /Y "%CONFIG_BASE%\BlenderBase" "%CONFIG_PATH%"
        echo [OK] Copied BlenderBase to %CONFIG_PATH%
    ) else (
        echo [ERROR] BlenderBase does not exist at %CONFIG_BASE%
        exit /b 1
    )
)

:: Set Blender config and scripts path
set "BLENDER_USER_CONFIG=%CONFIG_PATH%\blenderconfig"
set "BLENDER_USER_SCRIPTS=%CONFIG_PATH%\blenderscripts"

:: Create folders if missing
if not exist "%BLENDER_USER_CONFIG%" mkdir "%BLENDER_USER_CONFIG%"
if not exist "%BLENDER_USER_SCRIPTS%" mkdir "%BLENDER_USER_SCRIPTS%"

:: Launch Blender with script
start "" "C:\Program Files\Blender Foundation\%FolderName%\blender.exe" --python "BlenderForceGpuConfig.py"
