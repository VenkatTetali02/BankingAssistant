from db.models import Customer,CustomerAccount
from sqlalchemy import and_,func
from db.database import get_db

class CustomerAccountRepository:
    def __init__(self,db=next(get_db())):
        self.db=db

    def get_all_customer_accounts(self,skip=0,limit=100):
        customer_accounts=self.db.query(CustomerAccount).offset(skip).limit(limit).all()
        print(customer_accounts)
        if customer_accounts:
            return customer_accounts
    
    def get_customer_accounts(self,cust_id):
        cust_accounts=self.db.query(CustomerAccount).filter(CustomerAccount.CustID==cust_id).all()
        if cust_accounts:
            print(cust_accounts)
            return True,cust_accounts
        return False,f'Customer {cust_id} Not Found'
    
    def get_account_balance(self,cust_id,acct_type):
        cust_account=self.db.query(CustomerAccount).filter(and_(CustomerAccount.CustID==cust_id,CustomerAccount.AccountType==acct_type)).first()
        if cust_account:
            print(cust_account)
            return True,cust_account
        return False,{"Balance":0,"name":"Not Found"}
    
    def create_customer_account(self,cust_id,acct_type, balance):
        custaccount=self.db.query(CustomerAccount).filter(and_(CustomerAccount.CustID==cust_id,CustomerAccount.AccountType==acct_type)).first()
        if not custaccount:
            accountnum=self.db.query(func.max(CustomerAccount.AccountNum)).scalar()
        else:
            return False,f"{acct_type} already exits for Customer {cust_id}"
        
        if not accountnum:
            accountnum=0

        customer=self.db.query(Customer).filter(Customer.id==cust_id).first()
        new_cust_account=CustomerAccount(CustID=cust_id,AccountNum=accountnum+1,AccountType=acct_type,Balance=balance,owner=customer)
        self.db.add(new_cust_account)
        self.db.commit()
        self.db.refresh(new_cust_account)
        return True, new_cust_account
    
    def update_customer_account(self,cust_id,acct_type,balance):
        cust_acct_record=self.db.query(CustomerAccount).filter(and_(CustomerAccount.CustID==cust_id,CustomerAccount.AccountType==acct_type)).first()
        if cust_acct_record:
            cust_acct_record.Balance=balance
            self.db.commit()
            self.db.refresh(cust_acct_record)
            return True,'Customer Account updated'
        
        return  False,f'Customer Account with Cust ID {cust_id} Not updated'
    
    def delete_customer_account(self,cust_id,acct_type):
        cust_acct_record=self.db.query(CustomerAccount).filter(and_(CustomerAccount.id==cust_id,CustomerAccount.AccountType==acct_type)).first()
        if cust_acct_record:
            self.db.delete(cust_acct_record)
            self.db.commit()