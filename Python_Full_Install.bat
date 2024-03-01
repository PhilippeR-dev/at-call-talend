@echo off
cd /d "%~dp0"
::  Python Installation
:: creation des variables BatchPath et InstallPath
set InstallPath=%cd%\install
echo InstallPath = %InstallPath%
set PythonPath=%cd%\python
echo PythonPath = %PythonPath%
:: Installation des Packages en pré-requis

REM Vérifier si le répertoire %PythonPath% existe déjà
if exist "%PythonPath%" (
    echo Le repertoire %PythonPath% existe deja.
    @REM echo Desinstallation de l'ancienne version de Python...
    @REM %PythonPath%\python-3.11.7-amd64.exe /quiet Uninstall /force
    echo Desinstallation complete de l'ancienne version de Python...
    echo %PythonPath%\python-3.11.7-amd64.exe /quiet removeall
    %PythonPath%\python-3.11.7-amd64.exe /quiet removeall
    echo Suppression du repertoire %PythonPath%...
    rd /s /q "%PythonPath%"
)

:: creation du repertoire avec Python
echo Creation du repertoire %PythonPath%...
mkdir "%PythonPath%"

:: Décompression du fichier python-3.11.7-amd64.zip
cd /d %InstallPath%
powershell -command Expand-Archive -Path python-3.11.7-amd64.zip -DestinationPath %PythonPath%

:: Installation de l interpreteur Python
echo Debut Installation Python interpreteur
::ren %InstallPath%\python-3.11.7-amd64.exe.txt python-3.11.7-amd64.exe
echo Installation de Python et de pip en cours...
echo %PythonPath%\python-3.11.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 InstallLauncherAllUsers=1 TargetDir=%PythonPath%\ 
%PythonPath%\python-3.11.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 InstallLauncherAllUsers=1 TargetDir=%PythonPath%\
echo Fin Installation Python interpreteur

:: Installation des Packages en pré-requis
%PythonPath%\python.exe -m pip install --upgrade pip
%PythonPath%\python.exe -m pip install -r %InstallPath%\requirements.txt
pause