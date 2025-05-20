::@echo off
setlocal enabledelayedexpansion

:: Path to .env
set "ENV_FILE=..\config.env"

:: default value (fallback)
set "ENV_STATE=PROD"

if exist "%ENV_FILE%" (
    for /f "usebackq tokens=1,2 delims== " %%A in ("%ENV_FILE%") do (
        if /I "%%A"=="STATE" (
            set "ENV_STATE=%%B"
        )
    )
) else (
    echo [INFO] config.env not found, defaulting to PROD mode.
)

:: Nettoyage des espaces éventuels
set "ENV_STATE=%ENV_STATE: =%"

:: Debug
echo Environment state: %ENV_STATE%

:: Maybe useless, check for the futur to optimize
set "CONFIG_PATH=..\"
:: Debug
:: echo État détecté : %ENV_STATE%
:: echo Chemin configuré : %CONFIG_PATH%
:: pause

:: Definition du dossier de userconfig et scripts
SET BLENDER_USER_CONFIG=%CONFIG_PATH%blenderconfig
SET BLENDER_USER_SCRIPTS=%CONFIG_PATH%blenderscripts

:: Debug
:: echo %BLENDER_USER_CONFIG%
:: echo %BLENDER_USER_SCRIPTS%
:: pause

if not exist %BLENDER_USER_CONFIG% mkdir %BLENDER_USER_CONFIG%
if not exist %BLENDER_USER_SCRIPTS% mkdir %BLENDER_USER_SCRIPTS%

:: Path to Blender on local machine through deadline
start "" "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe" --python "BlenderForceGpuConfig.py"
