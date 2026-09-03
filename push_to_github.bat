@echo off
setlocal enabledelayedexpansion
echo ===================================================
echo   Pushing AI Sales Predictor to GitHub...
echo ===================================================
echo.
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\Git\mingw64\bin;%PATH%"

git remote set-url origin https://github.com/ayeshasiddiqua111111111-commits/AI-Sales-Predictor.git >nul 2>&1
if %errorlevel% neq 0 (
    git remote add origin https://github.com/ayeshasiddiqua111111111-commits/AI-Sales-Predictor.git
)

echo Adding files...
git add .
git commit -m "feat: complete AI Sales Predictor project files for Vercel" >nul 2>&1

echo.
echo Pushing to GitHub (a browser window may open once to authorize GitHub)...
git push -u --force origin main

if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo   SUCCESS! Pushed all files to GitHub!
    echo ===================================================
    echo.
    echo Now on Vercel:
    echo 1. Go to your Vercel project dashboard
    echo 2. Click "Redeploy" (or re-import)
    echo 3. Ensure Root Directory is set to "frontend"
    echo 4. Your site will be live!
) else (
    echo.
    echo Pushing failed. Please check the error above.
)

echo.
pause
