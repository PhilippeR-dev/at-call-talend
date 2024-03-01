import os, sys
import time, datetime, timedelta
import requests
import json
import logging
import base64

B_TRACE_LOG=False
WAIT_TIME_TO_SCAN_STATUS = 10 # seconds // for tests
WAIT_TIME_TO_FETCH_LOGS = 15 # seconds // for tests
PRINT_STATUS_TIME = 30 # seconds // for tests
DELTA_TIMEOUT = 3600 # 3600 seconds or 1 hour // for tests


def print_if_trace(message, trace=False):
    """
    Imprime le message spécifié si le paramètre trace est True.

    Args:
        message (str): Le message à imprimer.
        trace (bool, optional): Indique si le message doit être imprimé ou non.
                                Par défaut, False.
    """
    if trace:
        print(message)
        
def generate_access_token(client_id, client_secret, last_token_generated=None):
    # Vérifier si la date et l'heure de la dernière génération de token ont été fournies
    if last_token_generated is not None:
        # Calculer la différence de temps entre maintenant et la dernière génération de token
        time_difference = datetime.datetime.now() - last_token_generated

        # Si la différence de temps est inférieure à 25 minutes, renvoyer le token existant
        if time_difference < timedelta.Timedelta(minutes=25):
            mynow=datetime.datetime.now().isoformat()
            message='Talend Compte de Service - Génération du Service Access Token - Utilisation du token existant'
            print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)
            return None

    # Endpoint de l'API Talend pour la génération de token
    token_endpoint = f"{TALEND_API_URL}/security/oauth/token"

    # Encodage en Base64 du client_id et client_secret
    encoded_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    # En-têtes de la demande pour la génération de token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    # Données de demande pour la génération de token
    payload = {
        'audience': f"{TALEND_API_URL}",
        'grant_type': 'client_credentials'
    }

    try:
        # Effectuer une requête POST pour obtenir un nouveau token
        response = requests.post(token_endpoint, headers=headers, json=payload)
        response.raise_for_status()  # Vérifier si la requête a réussi

        # Extraire le token d'accès du corps de la réponse JSON
        access_token = response.json()['access_token']

        # Renvoyer le token d'accès généré
        return access_token

    except requests.exceptions.RequestException as error:
        mynow=datetime.datetime.now().isoformat()
        message='Talend Compte de Service - Erreur lors de la génération du Service Access Token :'+error
        logging.error(message)
        print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)
        return None
        
def _get_task_info() -> str:

    urlGetInfo = f"{TALEND_API_URL}/orchestration/executables/tasks/{TALEND_TASK_ID}"  # TALEND_API_URL = https://api.eu.cloud.talend.com

    headers = {
        'Accept': 'application/json',
        'Authorization': f"Bearer {TALEND_API_KEY}",
    }
    response = requests.request("GET", urlGetInfo, headers=headers)

    statusGI_code=response.status_code
    if statusGI_code != 200:
        message='Talend Task > Get Info < is failed !!! - status_code: '+str(statusGI_code)
        logging.error(message)
        mynow=datetime.datetime.now().isoformat()
        raise Exception(f"{mynow} - {message}")
    else:
        data = json.loads(response.content)
        return data['name']

def _trigger_task(task_name) -> str:

    urlRUN = f"{TALEND_API_URL}/processing/executions"  # TALEND_API_URL = https://api.eu.cloud.talend.com
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Bearer {TALEND_API_KEY}",
    }
    payload = json.dumps({
        "executable": f"{TALEND_TASK_ID}",
        "logLevel": "INFO"
    })
    
    response = requests.post(urlRUN, headers=headers, data=payload)

    execution_id = ''
    statusRUN_code=response.status_code
    if statusRUN_code != 201:
        message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} > POST RUN < is failed !!! - status_code: "+str(statusRUN_code)
        logging.error(message)
        mynow=datetime.datetime.now().isoformat()
        raise Exception(f"{mynow} - {message}")
    else:
        data = json.loads(response.content)
        execution_id=data['executionId']
    
    return execution_id

def _get_task_logs(task_name, execution_id) -> str:

    urlLOGS = f"{TALEND_API_URL}/monitoring/executions/{execution_id}/logs"  # TALEND_API_URL = https://api.eu.cloud.talend.com/tmc/v2.6
    headers = {
        'Accept': 'application/json',
        'Authorization': f"Bearer {TALEND_API_KEY}",
    }
    params = {
        "id": execution_id,
        "startIndex": 0,
        "count": 50,
        "order": "DESC"
    }
    time.sleep(WAIT_TIME_TO_FETCH_LOGS)
    url = urlLOGS
    trueReturnCode=0
    while url:
        response = requests.get(url, params=params, headers=headers)
        statusGL_code=response.status_code
        if statusGL_code != 200:
            message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} + -> execution : {execution_id} > GET TALEND LOGS < is failed !!! :( - status_code: "+str(statusGL_code)
            logging.error(message)
            mynow=datetime.datetime.now().isoformat()
            raise Exception(f"{mynow} - {message}")
        else:
            data = response.json()
            message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} -> execution : {execution_id} > GET TALEND LOGS < is completed successfully :) - status_code: "+str(statusGL_code)+" - page n°"+str(params['startIndex'])
            logging.info(message)
            mynow=datetime.datetime.now().isoformat()
            print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)
            logs=data["data"]
            for log in logs:
                #logprint=json.dumps(log, indent=4, ensure_ascii=False)
                #logging.info(logprint)
                #varprint=log["logMessage"]
                #print_if_trace(f"{mynow} - {logprint}",B_TRACE_LOG)
                lgmessage=log["logMessage"]
                if 'CUSTOM_STATUS_CODE' in lgmessage:
                    message= '<<< RETURN CODE IN THE LOGS >>> '+ lgmessage
                    logging.info(message)
                    print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)
                    trueReturnCode = lgmessage.strip().split("=")[1]
                    #print_if_trace(trueReturnCode,B_TRACE_LOG)
                #print_if_trace(f"{mynow} - {logprint}",B_TRACE_LOG)             
            # Check if there's a next page using nextIndex
            next_index = data.get('nextIndex', None)
            if next_index is not None:
                params['startIndex'] = next_index
            else:
                url = None  # No more pages to fetch
    
    return trueReturnCode

def run():
    
    global TALEND_API_KEY
    global LAST_SAT_GENERATED
    LAST_SAT_GENERATED = None  
    sat = generate_access_token(TALEND_CLIENT_ID,TALEND_CLIENT_PWD,LAST_SAT_GENERATED)
    if sat:
        TALEND_API_KEY = sat
        LAST_SAT_GENERATED = datetime.datetime.now()
        mynow=datetime.datetime.now().isoformat()
        message='Talend Compte de Service - Nouveau token généré  ' #+sat
        logging.error(message)
        print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)
    
    #print(' TALEND_API_KEY =  ', TALEND_API_KEY)
    
    task_name = _get_task_info()
    
    task_execution_id = _trigger_task(task_name)
    
    message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} > RUN < -> execution : {task_execution_id} is started "
    logging.info(message)
    mynow=datetime.datetime.now().isoformat()
    print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)
    
    urlGS = f"{TALEND_API_URL}/processing/executions/{task_execution_id}"

    timeout = time.time() + DELTA_TIMEOUT  
    waitingtime = WAIT_TIME_TO_SCAN_STATUS
    timeprint = time.time() + PRINT_STATUS_TIME    

    while True:
        time.sleep(waitingtime)
        
        sat = generate_access_token(TALEND_CLIENT_ID,TALEND_CLIENT_PWD,LAST_SAT_GENERATED)
        if sat:
            TALEND_API_KEY = sat
            LAST_SAT_GENERATED = datetime.datetime.now()
            mynow=datetime.datetime.now().isoformat()
            message='Talend Compte de Service - Nouveau token généré : '+sat
            logging.error(message)
            print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)
        
        response = requests.request("GET", urlGS, headers={ 'Authorization': f"Bearer {TALEND_API_KEY}" }, data={})
        
        statusGS_code=response.status_code
        data = json.loads(response.content)
        exec_status=data['status']
        execution_status=data['executionStatus']
        if statusGS_code != 200:
            message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} > RUN < -> execution : {task_execution_id} is failed (GS<>200) !!! - status_code: "+str(statusGS_code)+' - exec_status : '+exec_status+' - execution_status : '+execution_status
            logging.error(message)
            mynow=datetime.datetime.now().isoformat()
            raise Exception(f"{mynow} - {message}")
        #
        # LOV executionStatus : 
        #       EXECUTION_EVENT_RECEIVED, DISPATCHING_FLOW, 
        #       STARTING_FLOW_EXECUTION, STOPPING_FLOW_EXECUTION, 
        #       EXECUTION_TERMINATED, 
        #       EXECUTION_TERMINATED_TIMEOUT, 
        #       DEPLOY_FAILED, EXECUTION_FAILED, 
        #       EXECUTION_REJECTED, 
        #       EXECUTION_SUCCESS 
        # LOV status
        #       dispatching, deploy_failed, 
        #       executing, execution_successful, 
        #       execution_rejected, execution_failed, 
        #       terminated, terminated_timeout 
        #
        elif exec_status == 'execution_successful' or execution_status == 'EXECUTION_SUCCESS':
            message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} > RUN < -> execution : {task_execution_id} is completed successfully :) - status_code: "+str(statusGS_code)+' - exec_status : '+exec_status+' - execution_status : '+execution_status
            logging.info(message)
            mynow=datetime.datetime.now().isoformat()
            print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)           
            break
        elif time.time() > timeout:
            message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} > RUN < -> execution : {task_execution_id} is running but timeout !!! :( - exec_status : "+exec_status+' - execution_status : '+execution_status
            logging.error(message)
            mynow=datetime.datetime.now().isoformat()
            print_if_trace(f"{mynow} - {message}",B_TRACE_LOG) 
            break
        elif exec_status == 'executing' or exec_status == 'dispatching':
            if time.time() > timeprint:
                message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} > RUN < -> execution : {task_execution_id} is running - status_code: "+str(statusGS_code)+' - exec_status : '+exec_status+' - execution_status : '+execution_status
                logging.error(message)
                mynow=datetime.datetime.now().isoformat()
                print_if_trace(f"{mynow} - {message}",B_TRACE_LOG) 
                timeprint = time.time() + PRINT_STATUS_TIME
        else:
            message=f"Talend Task id : {TALEND_TASK_ID} - {task_name} > RUN < -> execution : {task_execution_id} is failed (GS other) !!! - status_code: "+str(statusGS_code)+' - exec_status : '+exec_status+' - execution_status : '+execution_status
            logging.error(message)
            mynow=datetime.datetime.now().isoformat()
            raise Exception(f"{mynow} - {message}")
    
    sat = generate_access_token(TALEND_CLIENT_ID,TALEND_CLIENT_PWD,LAST_SAT_GENERATED)
    if sat:
        TALEND_API_KEY = sat
        LAST_SAT_GENERATED = datetime.datetime.now()
        mynow=datetime.datetime.now().isoformat()
        message='Talend Compte de Service - Nouveau token généré : '+sat
        logging.error(message)
        print_if_trace(f"{mynow} - {message}",B_TRACE_LOG)
            
    code = _get_task_logs(task_name,task_execution_id)
    return code
        
if __name__ == '__main__':
    
    mynow=datetime.datetime.now().isoformat()
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d-%H-%M-%S') 
    print_if_trace(f"{mynow} - START TALEND LAUNCHER",B_TRACE_LOG)
    TALEND_API_URL = sys.argv[1]
    #TALEND_API_KEY = sys.argv[2]
    TALEND_CLIENT_ID = sys.argv[2]
    TALEND_CLIENT_PWD = sys.argv[3]
    TALEND_TASK_ID = sys.argv[4]
    LOGS_FOLDER = sys.argv[5]
    B_TRACE_LOG = (sys.argv[6].lower() == "true")
    #LOGS_FILE_NAME = 'talend_task_'+str(TALEND_TASK_ID)+'_'+str(formatted_datetime)+'.log'
    LOGS_FILE_NAME = 'talend_task_'+str(TALEND_TASK_ID)+'.log'
    print_if_trace(str(mynow)+' - parameter > TALEND_API_URL : '+TALEND_API_URL,B_TRACE_LOG)
    #print_if_trace(str(mynow)+' - parameter > TALEND_API_KEY : '+TALEND_API_KEY,B_TRACE_LOG)
    print_if_trace(str(mynow)+' - parameter > TALEND_CLIENT_ID : '+TALEND_CLIENT_ID,B_TRACE_LOG)
    print_if_trace(str(mynow)+' - parameter > TALEND_TASK_ID : '+TALEND_TASK_ID,B_TRACE_LOG)
    print_if_trace(str(mynow)+' - parameter > LOGS_FOLDER : '+LOGS_FOLDER,B_TRACE_LOG)
    print_if_trace(str(mynow)+' - parameter > LOGS_FILE_NAME : '+LOGS_FILE_NAME,B_TRACE_LOG)
    
    logfolder=LOGS_FOLDER.replace('\\', '/').strip()
    fulllogfile=logfolder+LOGS_FILE_NAME
    logging.basicConfig(filename=fulllogfile,
							format='%(asctime)s %(levelname)s:%(message)s',
							datefmt='%Y-%m-%d %I:%M:%S %p',
							level=logging.INFO)
    
    logging.info("-------------------------------------------------------------")
    logging.info("START TALEND LAUNCHER")
    rcode = run()
    logging.info("END TALEND LAUNCHER")
    logging.info("-------------------------------------------------------------")
    print_if_trace(f"{mynow} - END TALEND LAUNCHER",B_TRACE_LOG)
    sys.exit(int(rcode))