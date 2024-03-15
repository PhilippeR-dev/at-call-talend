@echo off
cd /d "%~dp0"
setlocal enabledelayedexpansion

rem Obtenir la date et l'heure actuelles
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a

rem Extraire les parties nécessaires de la date et de l'heure
set year=!datetime:~0,4!
set month=!datetime:~4,2!
set day=!datetime:~6,2!
set hour=!datetime:~8,2!
set minute=!datetime:~10,2!
set second=!datetime:~12,2!

echo %year%-%month%-%day% %hour%:%minute%:%second% - Start - Talend Launcher
set PythonPath=%cd%\python\
:: echo PythonPath = %PythonPath%
set pathTalendLauncher=%cd%
:: echo pathTalendLauncher=%pathTalendLauncher%
set talendApiUrl=https://api.eu.cloud.talend.com
set talendCliendID="pvKbM26xj4zDocIwwJ-XCZB6QLJVj2rPSy8KB5C_-aA"
set talendCliendPWD="?? mot de pase du Service Account"
:: Task Id for the job Log_test_synergy
set talendtaskId="65c0aeccca7ada2633706517" 
set logsFolder=%cd%\logs\
set traceLog=True 

cd /d %PythonPath%
:: echo cd = %cd%
python.exe %pathTalendLauncher%\talend_launcher.py %talendApiUrl% %talendCliendID% %talendCliendPWD% %talendtaskId% %logsFolder% %traceLog%
set PYTHON_EXIT_CODE=%ERRORLEVEL%
echo %PYTHON_EXIT_CODE%

rem Obtenir la date et l'heure actuelles
for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a

rem Extraire les parties nécessaires de la date et de l'heure
set year=!datetime:~0,4!
set month=!datetime:~4,2!
set day=!datetime:~6,2!
set hour=!datetime:~8,2!
set minute=!datetime:~10,2!
set second=!datetime:~12,2!

echo %year%-%month%-%day% %hour%:%minute%:%second% - End - Talend Launcher
endlocal
pause