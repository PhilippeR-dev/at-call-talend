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
:: Installation de l interpreteur Python
echo Debut Installation Python interpreteur
%InstallPath%\python-3.11.7-amd64.exe quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%PythonPath%
echo Fin Installation Python interpreteur

cd /d %PythonPath%
:: Installation des Packages en pré-requis
python.exe pip install -r %InstallPath%\requirements.txt
pause