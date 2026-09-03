@echo off
setlocal enabledelayedexpansion
echo ========================================================
echo   Pushing AI Sales Predictor (Next.js) to GitHub...
echo ========================================================
echo.
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\Git\mingw64\bin;%PATH%"

git remote set-url origin https://github.com/ayeshasiddiqua111111111-commits/AI-Sales-Predictor.git >nul 2>&1
if %errorlevel% neq 0 (
    git remote add origin https://github.com/ayeshasiddiqua111111111-commits/AI-Sales-Predictor.git
)

echo Adding latest files...
git add .
git commit -m "feat: complete Next.js deployment" >nul 2>&1

echo.
echo Pushing to GitHub (a GitHub login dialog will appear if not signed in)...
git push -u --force origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo   SUCCESS! All Next.js files are now on GitHub!
    echo ========================================================
    echo.
    echo Now Vercel will automatically deploy, or click Redeploy!
) else (
    echo.
    echo Pushing encountered an issue. See above.
)

echo.
pause
