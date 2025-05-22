@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

set "baseDir=C:\Program Files\Blender Foundation"
echo Recherche des versions Blender 4.X dans %baseDir%
echo.

REM Parcourir les sous-dossiers Blender 4.*
for /D %%D in ("%baseDir%\Blender 4.*") do (
    set "folderPath=%%~fD"
    set "folderName=%%~nxD"

    REM Extraire la version depuis le nom du dossier
    for /f "tokens=2 delims= " %%V in ("!folderName!") do (
        set "version=%%V"
    )

    set "fileName=blender_!version!_deadline.bat"
    set "remoteFile=https://raw.githubusercontent.com/FoligrafAurelien/BlenderAutoConfig_Deadline/main/bat/blender_deadline.bat"
    set "localPath=!folderPath!\!fileName!"

    echo [+] Téléchargement de !fileName! dans !folderPath!...
    powershell -Command "Invoke-WebRequest -Uri '!remoteFile!' -OutFile '!localPath!' -UseBasicParsing"
    if exist "!localPath!" (
    	echo [✓] Téléchargé avec succès : !localPath!
    ) else (
    	echo [!] Échec du téléchargement depuis : !remoteFile!
    )
)
