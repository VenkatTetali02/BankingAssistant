from fastapi import APIRouter, Request
from utils.sessions import *
from intents.accounts import Accounts

router=APIRouter(prefix="/bot",tags=['Chatbot'])

@router.post("/")
async def respond_back(request:Request):
    payload=await request.json()
    intent=payload['queryResult']['intent']['displayName']
    action=payload['queryResult']['action']
    if action=="UserInput-User":
        responseText=store_userid(payload)
    elif action=="UserInput-Passcode":
        status ,message=validate_passcode(payload)
        if status:
            accountsObj=Accounts()
            responseText=accountsObj.get_balances(payload)
        else:
            responseText=message
    if action=='UserInput-AccountType':
        store_account_type(payload)
        status, message=verify_login(payload)
        if status:
            accountsObj=Accounts()
            responseText=accountsObj.get_balances(payload)
        else:
            responseText=message
    elif intent=="Entering Passcode":
         pass
    return {"fulfillmentText":responseText}

@router.get("/")
def bot_get(request:Request):
    print('in bot request')
    return {"fulfillmentText":"Received the request"}