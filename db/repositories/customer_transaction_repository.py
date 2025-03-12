from db.models import Customer,CustomerAccount,CustomerTransaction
from sqlalchemy import and_
from db.database import get_db

class CustomerTransactionRepository:
    def __init__(self,db=next(get_db())):
        self.db=db
    
    def create_customer_transaction(self,accountnum,amount,description):
        customer_account=self.db.query(CustomerAccount).filter(CustomerAccount.AccountNum==accountnum).first()
        cust_transaction=CustomerTransaction(AccountNum=accountnum,Amount=amount,Description=description,cust_account=customer_account)
        self.db.add(cust_transaction)
        self.db.commit()
        self.db.refresh(cust_transaction)
        return True,cust_transaction
    
    def get_last_n_customer_transactions(self,cust_id,acct_type,count):
        result=self.db.query(Customer, CustomerAccount,CustomerTransaction).filter(Customer.id==cust_id).join(CustomerAccount,and_(CustomerAccount.AccountType==acct_type,CustomerAccount.CustID==Customer.id)).join(CustomerTransaction,CustomerAccount.AccountNum==CustomerTransaction.AccountNum).limit(count).all()
        final_str=''
        for _,_,cust_transaction in result:
        #    final_list.append({"Amount":cust_transaction.Amount,"Description":cust_transaction.Description,"TransactionDttm":cust_transaction.Created_At})
           final_str+=f'Transaction Amount is {cust_transaction.Amount} with the description {cust_transaction.Description} recorded on date {cust_transaction.Created_At}<br>'
        final_str='No Transactions Found' if final_str=='' else final_str
        return True, final_str

