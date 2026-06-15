@echo off

REM ==========================
REM PATHS (adjust per machine)
REM ==========================

set MAYAPY="C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe"
set BLENDER="C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"

REM ==========================
REM SCRIPTS
REM ==========================

set FOLDERPATHS_SCRIPT=%~dp0genDCCrootPath.py
set MAYA_SCRIPT=%~dp0MayaScenesGenerator\gen_mayaScenes.py
set BLENDER_SCRIPT=%~dp0BlenderScenesGenerator\gen_blenderScenes.py

echo Creating folder structure...
python %FOLDERPATHS_SCRIPT%

if %ERRORLEVEL% neq 0 (
    echo.
    echo ==========================
    echo   ERROR IN STRUCTURE BUILD
    echo ==========================
    pause
    exit /b
)

REM ==========================
REM STEP 2: MAYA
REM ==========================

echo Running Maya generator...
%MAYAPY% %MAYA_SCRIPT%

if %ERRORLEVEL% neq 0 (
    echo.
    echo ==========================
    echo   MAYA ERROR
    echo ==========================
    pause
    exit /b
)

REM ==========================
REM STEP 3: BLENDER
REM ==========================

echo Running Blender generator...
%BLENDER% -b --factory-startup --python %BLENDER_SCRIPT%

if %ERRORLEVEL% neq 0 (
    echo.
    echo ==========================
    echo   BLENDER ERROR
    echo ==========================
    pause
    exit /b
)

REM ==========================
REM DONE
REM ==========================

echo.
echo ==========================
echo   ALL DONE SUCCESSFULLY
echo ==========================

pause