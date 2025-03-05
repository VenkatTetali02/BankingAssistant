from db.database import get_db
from db.models import CustomerAccount
from sqlalchemy import and_,func

class CustomerAccountRepository:
    def __init__(self):
        self.db=next(get_db())
    
    def get_customer_account(self,cust_id,acct_type):
        return self.db.query(CustomerAccount).filter(and_(CustomerAccount.CustID==cust_id,CustomerAccount.AccountType==acct_type)).first()
    
    def get_customer_accounts(self,cust_id,skip=0,limit=100):
        return self.db.query(CustomerAccount).filter(CustomerAccount.CustID==cust_id).offset(skip).limit(limit).all()
    
    def create_customer_account(self,cust_id,acct_type, balance):
        custaccount=self.db.query(CustomerAccount).filter(and_(CustomerAccount.CustID==cust_id,CustomerAccount.AccountType==acct_type)).first()
        if not custaccount:
            accountnum=self.db.query(func.max(CustomerAccount.AccountNum)).scalar()
        else:
            return False,f"{acct_type} already exits for Customer {cust_id}"
        
        if not accountnum:
            accountnum=0

        new_cust_account=CustomerAccount(CustID=cust_id,AccountNum=accountnum+1,AccountType=acct_type,Balance=balance)
        self.db.add(new_cust_account)
        self.db.commit()
        self.db.refresh(new_cust_account)
        return True, new_cust_account
    
    def update_customer_account(self,cust_id,acct_type,balance):
        cust_acct_record=self.db.query(CustomerAccount).filter(and_(CustomerAccount.CustID==cust_id,CustomerAccount.AccountType==acct_type)).filter().first()
        if cust_acct_record:
            cust_acct_record.Balance=balance
            self.db.commit()
            self.db.refresh(cust_acct_record)

    def delete_customer(self,cust_id,acct_type):
        cust_acct_record=self.db.query(CustomerAccount).filter(and_(CustomerAccount.id==cust_id,CustomerAccount.AccountType==acct_type)).filter().first()
        if cust_acct_record:
            self.db.delete(cust_acct_record)
            self.db.commit()