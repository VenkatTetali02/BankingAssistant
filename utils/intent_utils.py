from data.sessionData import sessions
from utils.session_utils import get_session_id
from intents.accounts import Accounts

def store_account_type(payload):
    sessionId=get_session_id(payload)
    acct_type=payload['queryResult']['parameters']['AccountType']
    sessions[sessionId]['AccountType']=acct_type
    sessions[sessionId]["last-intent"]=payload['queryResult']['action']
    print('Account type',sessions)

def store_requested_history_data(payload):
    sessionId=get_session_id(payload)
    acct_type=payload['queryResult']['parameters']['AccountType'][0]
    days=payload['queryResult']['parameters']['number-integer']
    sessions[sessionId]['AccountType']=acct_type
    sessions[sessionId]['lastN']=days
    sessions[sessionId]["last-intent"]=payload['queryResult']['action']


def verify_login(payload):
    sessionId=get_session_id(payload)
    sessionIdDict=sessions[sessionId]
    if 'user' in sessionIdDict.keys() and 'authenticated' in sessionIdDict.keys():
        return True , "User Authenticated"
    
    return  False, "Please login with your UserID" 

def store_userid(payload):
     sessionId=get_session_id(payload)
     cust_id=payload['queryResult']['parameters']['any']
     current_cust_id=sessions[sessionId].get('user','NF')
     if current_cust_id!=cust_id:
         if 'authenticated' in sessions[sessionId].keys():
             del sessions[sessionId]['authenticated']
     sessions[sessionId]['user']=cust_id

     return "Please enter your passcode"

def execute_last_intent(payload):
     sessionId=get_session_id(payload)
     last_intent=sessions[sessionId]["last-intent"]
     if last_intent=='UserInput-History':
         print('In User Intent UserInput-History')
         accountIntent=Accounts()
         ret_status,message=accountIntent.get_last_n_transactions(payload)
         return ret_status, message
     
     if last_intent=='UserInput-AccountType':
         accountIntent=Accounts()
         ret_status,message=accountIntent.get_balances(payload)
         return ret_status, message
     
     return True,'Feel Free to inquire about Past Transactions, Account Balances etc'