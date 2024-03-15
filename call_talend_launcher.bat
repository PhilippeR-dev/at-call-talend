@echo off
cd /d "%~dp0"

set PythonPath=%cd%\python\
:: echo PythonPath = %PythonPath%
set pathTalendLauncher=%cd%
:: echo pathTalendLauncher=%pathTalendLauncher%
set talendApiUrl=https://api.eu.cloud.talend.com
set talendCliendID="pvKbM26xj4zDocIwwJ-XCZB6QLJVj2rPSy8KB5C_-aA"
set talendCliendPWD="?? mot de pase du Service Account"
:: Task Id for the job
set talendtaskId="??? Task Id ???" 
set logsFolder=%cd%\logs\
set traceLog=False 

cd /d %PythonPath%
:: echo cd = %cd%
python.exe %pathTalendLauncher%\talend_launcher.py %talendApiUrl% %talendCliendID% %talendCliendPWD% %talendtaskId% %logsFolder% %traceLog%
set PYTHON_EXIT_CODE=%ERRORLEVEL%
echo %PYTHON_EXIT_CODE%