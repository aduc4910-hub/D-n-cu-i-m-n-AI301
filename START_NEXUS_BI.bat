@echo off
chcp 65001 >nul
title NexusBI Launcher
cd /d "%~dp0"

echo ===================================================
echo     ✦ KHỞI ĐỘNG HỆ THỐNG NEXUSBI PLATFORM ✦
echo ===================================================
echo.

set PYTHON_EXE=C:\Users\Lenovo\AppData\Local\antigravity\python\5a1c45aafcb841ee\python.exe
set PYTHONW_EXE=C:\Users\Lenovo\AppData\Local\antigravity\python\5a1c45aafcb841ee\pythonw.exe

:: Kiểm tra port 8080 xem server đã chạy chưa
netstat -ano | findstr ":8080" | findstr "LISTENING" >nul
if %ERRORLEVEL% EQU 0 (
    echo [✓] Server NexusBI đã đang chạy sẵn trên cổng 8080.
) else (
    echo [i] Đang khởi động Server NexusBI trên cổng 8080...
    if exist "%PYTHONW_EXE%" (
        start "" "%PYTHONW_EXE%" -u server.py 8080
    ) else if exist "%PYTHON_EXE%" (
        start "NexusBI Server" /min "%PYTHON_EXE%" -u server.py 8080
    ) else (
        start "NexusBI Server" /min python -u server.py 8080
    )
    timeout /t 2 /nobreak >nul
    echo [✓] Khởi động Server thành công!
)

echo [i] Đang mở trình duyệt vào http://localhost:8080 ...
start "" "http://localhost:8080"

echo.
echo ===================================================
echo   Giao diện đã sẵn sàng! Bạn có thể đóng cửa sổ này.
echo ===================================================
timeout /t 3 >nul
exit
