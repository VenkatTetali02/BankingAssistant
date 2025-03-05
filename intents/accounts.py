from utils.sessions import *
from db.repositories.customer_accounts_repository import CustomerAccountRepository

class Accounts:
    def get_balances(self,payload):
       sessionId=get_session_id(payload)
       acct_type=sessions[sessionId]['AccountType']
       cust_id=sessions[sessionId]['user']
       if sessions[sessionId].get('AccountType','Not Found')=='Not Found':
            return 'Please Select from Checkings, Savings, Credit Card'
       else:
            print(sessions)
            cust_acct_repo=CustomerAccountRepository()
            cust_acct_record=cust_acct_repo.get_customer_account(cust_id,acct_type)
            if cust_acct_record:
                del sessions[sessionId]['AccountType']
                return f"{acct_type} Account Balance is {cust_acct_record.Balance}"
            else:
                return "Customer ID or Account Type does not exist"
           
               

