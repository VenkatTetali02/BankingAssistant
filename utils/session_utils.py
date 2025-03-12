from utils.hashing import Hashing
from db.repositories.customer_repository import CustomerRepository
from data.sessionData import sessions

def get_session_id(payload):
    sessionId=payload['session'].split('/')[4]
    if sessionId not in sessions.keys():
        sessions[sessionId]={}
    return sessionId

def clear_session_data(payload):
     sessionId=get_session_id(payload)
     sessions[sessionId]={}
     del sessions[sessionId]
     return 'Exit Successful'

def verify_login(payload):
    sessionId=get_session_id(payload)
    sessionIdDict=sessions[sessionId]
    if 'user' in sessionIdDict.keys() and 'authenticated' in sessionIdDict.keys():
        return True , "User Authenticated"
    return  False, "Please login with your UserID" 

def validate_passcode(payload):
     sessionId=get_session_id(payload)
     passcode=payload['queryResult']['parameters']['any']
     cust_id=sessions[sessionId]['user']
     customer_repository=CustomerRepository()
     ret_status,customerrecord=customer_repository.get_customer(cust_id)
     hashing=Hashing()
     result=hashing.verify(passcode,customerrecord.Passcode)

     if result:
         sessions[sessionId]['authenticated']=True
         return True , 'Successful Validation'
     else:
         return False ,'Invalid Passcode please try again'



 