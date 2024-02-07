@echo off
cd /d "%~dp0"
::  Python Installation
:: creation des variables BatchPath et InstallPath
set InstallPath=%cd%\install
echo InstallPath = %InstallPath%
set PythonPath=%cd%\python
echo PythonPath = %PythonPath%
:: Installation des Packages en pré-requis
mkdir %PythonPath%
:: Décompression du fichier python-3.11.7-amd64.zip
cd /d %InstallPath%
powershell -command Expand-Archive -Path python-3.11.7-amd64.zip -DestinationPath %PythonPath%
:: Installation de l interpreteur Python
echo Debut Installation Python interpreteur
::ren %InstallPath%\python-3.11.7-amd64.exe.txt python-3.11.7-amd64.exe
%PythonPath%\python-3.11.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%PythonPath%\
echo Fin Installation Python interpreteur

:: Installation des Packages en pré-requis
%PythonPath%\python.exe -m pip install --upgrade pip
%PythonPath%\python.exe -m pip install -r %InstallPath%\requirements.txt
pause