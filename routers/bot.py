from fastapi import APIRouter, Request
from utils.session_utils import *
from utils.intent_utils import *
from intents.accounts import Accounts
from intents.generic_info import GenericInfo

router=APIRouter(prefix="/bot",tags=['Chatbot'])

@router.post("/")
async def respond_back(request:Request):
    payload=await request.json()
    intent=payload['queryResult']['intent']['displayName']
    action=payload['queryResult']['action']
    print(f'action is {action}')

    if action=="UserInput-User":
        responseText=store_userid(payload)

    if action=="UserInput-Passcode":
        ret_status ,message=validate_passcode(payload)
        if ret_status:
            ret_status,responseText=execute_last_intent(payload)
        else:
            responseText=message

    if action=='UserInput-AccountType':
        store_account_type(payload)
        status, message=verify_login(payload)
        if status:
            accountsObj=Accounts()
            ret_status,responseText=accountsObj.get_balances(payload)
        else:
            responseText=message

    if action=="UserInput-Generic-Info":
        generic_info=GenericInfo()
        responseText=generic_info.getGenericInfo(payload)
    
    if action=='UserInput-History':
        store_requested_history_data(payload)
        ret_status, message=verify_login(payload)
        if ret_status:
            accountsObj=Accounts()
            ret_status,responseText=accountsObj.get_last_n_transactions(payload)
        else:
            responseText=message
    
    if action=='UserInput-Exit':
        responseText=clear_session_data(payload)

    return {"fulfillmentText":responseText}

@router.get("/")
def bot_get(request:Request):
    print('in bot request')
    return {"fulfillmentText":"Received the request"}