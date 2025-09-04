@echo off
echo Windows Firewall Configuration for Django Development Server
echo ============================================================
echo.

echo Checking current Django server process...
netstat -ano | findstr ":8000"
echo.

echo Adding Windows Firewall rule for Django development server...
netsh advfirewall firewall add rule name="Django Dev Server" dir=in action=allow protocol=TCP localport=8000
echo.

echo Adding firewall rule for Python.exe...
netsh advfirewall firewall add rule name="Python Django" dir=in action=allow program="%SystemRoot%\System32\python.exe"
netsh advfirewall firewall add rule name="Python Django Alt" dir=in action=allow program="C:\Python39\python.exe"
netsh advfirewall firewall add rule name="Python Django Alt2" dir=in action=allow program="C:\Python310\python.exe"
netsh advfirewall firewall add rule name="Python Django Alt3" dir=in action=allow program="C:\Python311\python.exe"
netsh advfirewall firewall add rule name="Python Django Alt4" dir=in action=allow program="C:\Python312\python.exe"
echo.

echo Testing local connectivity...
curl -s http://127.0.0.1:8000/api/v1/health
echo.

echo Testing network interface connectivity...
curl -s http://0.0.0.0:8000/api/v1/health
echo.

echo Configuration complete! 
echo The Django server should now be accessible from Android emulator via http://10.0.2.2:8000
echo.
pause