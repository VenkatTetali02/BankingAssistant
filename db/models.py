
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float ,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

Base=declarative_base()

class Customer(Base):
    __tablename__= 'customers'
    id=Column(Integer,primary_key=True, index=True)
    Name=Column(String)
    Passcode=Column(String)
    accounts=relationship('CustomerAccount',back_populates='owner')

class CustomerAccount(Base):
    __tablename__='customer_accounts'
    CustID=Column(Integer,ForeignKey('customers.id'),primary_key=True,index=True,nullable=False)
    AccountNum=Column(Integer,unique=True,nullable=False)
    AccountType=Column(String,primary_key=True,index=True)
    Balance=Column(Float)
    owner=relationship("Customer",back_populates="accounts")
    trans=relationship('CustomerTransaction',back_populates='cust_account')

class CustomerTransaction(Base):
    __tablename__='customer_transactions'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    AccountNum=Column(Integer,ForeignKey(CustomerAccount.AccountNum))
    Amount=Column(Float)
    Description=Column(String)
    Created_At=Column(DateTime,default=datetime.utcnow)
    cust_account=relationship('CustomerAccount',back_populates='trans')
 

MODELS_MAP={
    'customer':Customer,
    'customeraccounts':CustomerAccount,
    'customertransactions':CustomerTransaction

}