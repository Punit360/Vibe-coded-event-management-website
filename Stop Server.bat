@echo off
title Stop EventVantage
echo ==============================================
echo        Stopping EventVantage Server...
echo ==============================================
echo.

taskkill /F /IM node.exe >nul 2>&1
echo.
echo Server shut down successfully.
echo You can safely close this window.
timeout /t 3 >nul
