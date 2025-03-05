
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float ,ForeignKey
from sqlalchemy.orm import relationship
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

MODELS_MAP={
    'customer':Customer,
    'customeraccounts':CustomerAccount

}