@echo off
cd /d "%~dp0"

set PythonPath=%cd%\python\
:: echo PythonPath = %PythonPath%
set pathTalendLauncher=%cd%
:: echo pathTalendLauncher=%pathTalendLauncher%
set talendApiUrl=https://api.eu.cloud.talend.com/tmc/v2.6
set talendApiKey="??? Token API ????"
:: Task Id for the job Log_test_synergy
set talendtaskId="??? Task Id ???" 
set logsFolder=%cd%\logs\
set traceLog=False 

cd /d %PythonPath%
:: echo cd = %cd%
python.exe %pathTalendLauncher%\talend_launcher.py %talendApiUrl% %talendApiKey% %talendtaskId% %logsFolder% %traceLog%
set PYTHON_EXIT_CODE=%ERRORLEVEL%
echo %PYTHON_EXIT_CODE%