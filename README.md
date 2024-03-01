# Lanceur de batchs Talend

## Installation de python et ses dépendances

> Exécuter le fichier "Python_Full_Install.bat" en tant qu'administrateur
>
> Pré-requis : Avoir accès au site https://pypi.org/ pour le téléchargement des librairies sur le serveur d'applications
>
> Note : Pour supprimer ou désinstaller votre python, il vaut mieux utiliser le mode intérartif. Faire clic droit sur le fichier .\python\python-3.11.7-amd64.exe et exécuter en tant qu'administrateur puis sélectionner Uninstall ensuite vous pouvez supprimer le sous répertoire python.

## Exécution du lanceur de task Talend par un ordonnanceur

* Modifier les variables d'environnements
* Renseigner le numéro de la Task Talend
* Exécuter le fichier "call_talend_launcher.bat" en tant qu'administrateur

## Exécution du lanceur de task Talend en mode test

* Modifier les variables d'environnements
* Renseigner le numéro de la Task Talend
* Exécuter le fichier "call_talend_launcher_test.bat" en tant qu'administrateur

### Documentation de Référence sur l'API Talend

* https://api.talend.com/apis/
* https://api.talend.com/apis/orchestration/2021-03/#operation_get-task-by-id
* https://api.talend.com/apis/processing/2021-03/#operation_execute-task
* https://api.talend.com/apis/processing/2021-03/#operation_get-task-execution-status
* https://api.talend.com/apis/execution-logs/2021-03/#operation_get-task-execution-logs
