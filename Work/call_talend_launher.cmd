@echo off
echo Start of the program - ? Description ?
set pathPython=C:\Python312\
set pathTalendLauncher=c:\Repos\call-talend\
set talendApiUrl=https://api.eu.cloud.talend.com/tmc/v2.6
set talendApiKey = "BswPcdFFTOqPHQKaZIYvKo4onidLI0d7cG0CWziMG-fZ8NnPIOIauaMi9cOxip1i"
set crmPlanId = "6710eb1e-d023-4d7c-9766-d8c0efa24a99"
set errorlevel = 0 

%pathPython%python.exe %pathTalendLauncher%talend_launcher.py %talendApiUrl% %talendApiKey% %crmPlanId%
If %errorlevel%
    echo %errorlevel%
Else
    echo %errorlevel%


echo End of the program - ? Description ? 
pause