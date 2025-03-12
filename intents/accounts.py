from db.repositories.customer_accounts_repository import CustomerAccountRepository
from db.repositories.customer_transaction_repository import CustomerTransactionRepository
from utils.session_utils import get_session_id
from data.sessionData import sessions

class Accounts:
    def get_balances(self,payload):
       sessionId=get_session_id(payload)
       acct_type=sessions[sessionId]['AccountType']
       cust_id=sessions[sessionId]['user']
       if sessions[sessionId].get('AccountType','Not Found')=='Not Found':
            return False,'Please Select from Checkings, Savings, Credit Card'
       
       cust_acct_repo=CustomerAccountRepository()
       ret_status,message=cust_acct_repo.get_account_balance(cust_id,acct_type)
       if ret_status:
            del sessions[sessionId]['AccountType']
            return True,f"{acct_type} Account Balance is {message.Balance}"
       
       return False,"Customer ID or Account Type does not exist"
    
    def get_last_n_transactions(self,payload):
        sessionId=get_session_id(payload)
        acct_type=sessions[sessionId]['AccountType']
        lastN=5 if sessions[sessionId].get('lastN','NA')=='NA' else sessions[sessionId]['lastN']
        cust_tran_repo=CustomerTransactionRepository()
        ret_status,message=cust_tran_repo.get_last_n_customer_transactions(sessions[sessionId]['user'],acct_type,lastN)
        return ret_status,message
    
        

           
               

