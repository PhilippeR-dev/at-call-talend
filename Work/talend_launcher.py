import os
import sys
import time
import requests
import json
import datetime

def _trigger_plan() -> str:

    urlRUN = f"{TALEND_API_URL}/executions/plans"  # TALEND_API_URL = https://api.eu.cloud.talend.com/tmc/v2.6
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Bearer {TALEND_API_KEY}",
    }
    payload = json.dumps({
        "executable": "{CRM_PLAN_ID}",
        "rerunOnlyFailedTasks": True
    })

    response = requests.post(urlRUN, headers=headers, data=payload)

    execution_id = ''
    statusRUN_code=response.status_code
    if statusRUN_code != 201:
        raise Exception('CRM Plan > RUN < is failed !!! - status_code: '+str(statusRUN_code))
    else:
        data = json.loads(response.content)
        execution_id=data['executionId']
    
    return execution_id

def run():
    plan_execution_id = _trigger_plan()
    
    mynow=datetime.datetime.now().isoformat()
    print(f"{mynow} - CRM Plan - execution : {plan_execution_id} is started ")
    
    urlGS = f"{TALEND_API_URL}/executions/plans/{plan_execution_id}"

    timeout = time.time() + 60*60*20 # 20 hours from now
    waitingtime = 5
    timeprint = time.time() + 60*5 # 5 minutes from now

    while True:
        time.sleep(waitingtime)
        
        response = requests.request("GET", urlGS, headers={ 'Authorization': f"Bearer {TALEND_API_KEY}" }, data={})
        
        statusGS_code=response.status_code
        data = json.loads(response.content)
        execution_status=data['executionStatus']
        if statusGS_code != 200:
            mynow=datetime.datetime.now().isoformat()
            raise Exception(str(mynow)+' - CRM Plan - execution : '+plan_execution_id+'> Get status < is failed !!! - status_code: '+str(statusGS_code))
        elif execution_status == 'FINISHED' or execution_status == 'EXECUTION_SUCCESS':
            mynow=datetime.datetime.now().isoformat()
            print(str(mynow)+' - CRM Plan - execution : '+plan_execution_id+' is completed successfully')
            break
        elif time.time() > timeout:
            mynow=datetime.datetime.now().isoformat()
            print(str(mynow)+' - CRM Plan - execution : '+plan_execution_id+' is running and timeout !!!')
            break
        elif execution_status == 'STARTED':
            if time.time() > timeprint:
                mynow=datetime.datetime.now().isoformat()
                print(str(mynow)+' - CRM Plan - execution : '+plan_execution_id+' is running')
                timeprint = time.time() + 60*5 # 5 minutes from now
        else:
            raise Exception(str(mynow)+' - CRM Plan - execution : '+plan_execution_id+'> Get status < is failed !!! - execution_status: '+ execution_status)
        
if __name__ == '__main__':
    TALEND_API_URL = sys.argv[1]
    TALEND_API_KEY = sys.argv[2]
    CRM_PLAN_ID = sys.argv[3]
    run()