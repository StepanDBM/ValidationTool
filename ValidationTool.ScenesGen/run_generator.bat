@echo off

REM ==========================
REM AUTO-DETECT MAYA
REM ==========================

set MAYAPY=

REM Try 64-bit Program Files
for /f "delims=" %%i in ('dir "C:\Program Files\Autodesk\Maya*" /ad /b /o-n 2^>nul') do (
    if exist "C:\Program Files\Autodesk\%%i\bin\mayapy.exe" (
        set MAYAPY="C:\Program Files\Autodesk\%%i\bin\mayapy.exe"
        goto :foundMaya
    )
)

REM Try 32-bit fallback (rare but safe)
for /f "delims=" %%i in ('dir "C:\Program Files (x86)\Autodesk\Maya*" /ad /b /o-n 2^>nul') do (
    if exist "C:\Program Files (x86)\Autodesk\%%i\bin\mayapy.exe" (
        set MAYAPY="C:\Program Files (x86)\Autodesk\%%i\bin\mayapy.exe"
        goto :foundMaya
    )
)

:foundMaya
if defined MAYAPY (
    echo Using MAYAPY: %MAYAPY%
) else (
    echo Maya NOT FOUND
)

REM ==========================
REM AUTO-DETECT BLENDER
REM ==========================

set BLENDER=

for /f "delims=" %%i in ('dir "C:\Program Files\Blender Foundation\Blender*" /ad /b /o-n') do (
    set BLENDER="C:\Program Files\Blender Foundation\%%i\blender.exe"
    goto :foundBlender
)

:foundBlender

if defined BLENDER (
    echo Using BLENDER: %BLENDER%
) else (
    echo Blender NOT FOUND - skipping Blender step
)

REM ==========================
REM SCRIPTS
REM ==========================

set FOLDERPATHS_SCRIPT=%~dp0genDCCrootPath.py
set MAYA_SCRIPT=%~dp0MayaScenesGenerator\gen_mayaScenes.py
set BLENDER_SCRIPT=%~dp0BlenderScenesGenerator\gen_blenderScenes.py

REM ==========================
REM STEP 1: FOLDER STRUCTURE
REM ==========================

echo.
echo Creating folder structure...
python %FOLDERPATHS_SCRIPT%

if %ERRORLEVEL% neq 0 (
    echo.
    echo ==========================
    echo   ERROR IN STRUCTURE BUILD
    echo ==========================
    exit /b 1
)

REM ==========================
REM STEP 2: MAYA (if available)
REM ==========================

if defined MAYAPY (
    echo.
    echo Running Maya generator...
    %MAYAPY% %MAYA_SCRIPT%

    if %ERRORLEVEL% neq 0 (
        echo.
        echo ==========================
        echo   MAYA ERROR
        echo ==========================
        exit /b 2
    )
) else (
    echo.
    echo Skipping Maya step.
)

REM ==========================
REM STEP 3: BLENDER (if available)
REM ==========================

if defined BLENDER (
    echo.
    echo Running Blender generator...
    %BLENDER% -b --factory-startup --python %BLENDER_SCRIPT%

    if %ERRORLEVEL% neq 0 (
        echo.
        echo ==========================
        echo   BLENDER ERROR
        echo ==========================
        exit /b 3
    )
) else (
    echo.
    echo Skipping Blender step.
)

REM ==========================
REM FINAL STATUS
REM ==========================

echo.
echo ==========================
echo   ALL DONE SUCCESSFULLY
echo ==========================

exit /b 0
