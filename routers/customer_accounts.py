from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List
from db import models
from db.database import get_db
from sqlalchemy.orm import Session
import schemas
from db.repositories.customer_accounts_repository import CustomerAccountRepository

router=APIRouter(prefix="/accounts",tags=['CustomerAccounts'])

@router.post("/customer")
def create_customer_accounts(request:schemas.CustomerAccountRequest,db:Session=Depends(get_db)):
    cust_account_repo=CustomerAccountRepository()
    status,message=cust_account_repo.create_customer_account(request.CustID,request.AccountType,request.Balance)
    if status:
        return message
    else:
        raise HTTPException(status.HTTP_409_CONFLICT,message)

@router.get("/customer",tags=['CustomerAccounts'],response_model=List[schemas.CustomerAccountResponse])
def get_customer_accounts(db:Session=Depends(get_db)):
   accounts=db.query(models.CustomerAccount).all()
   return accounts

@router.get("/customer/{cust_id}",response_model=List[schemas.CustomerAccountResponse])
def get_specific_customer_accounts(cust_id,request:schemas.CustomerAccountRequest,db:Session=Depends(get_db)):
   accounts=db.query(models.CustomerAccount).filter(models.CustomerAccount.CustID==request.cust_id).all()
   return accounts

@router.put("/customer/{cust_id}")
def update_specific_customer_accounts(cust_id,request:schemas.CustomerAccountUpdateRequest,db:Session=Depends(get_db)):
   cust_account=db.query(models.CustomerAccount).filter(models.CustomerAccount.CustID==cust_id and models.CustomerAccount.AccountType==request.AccountType and models.CustomerAccount.AccountNum==request.AccountNum)
   if not cust_account.first():
         raise HTTPException(status.HTTP_404_NOT_FOUND,f"Customer with ID {cust_id} not found")
   else:
         cust_account.update({"Balance":request.Balance})
         db.commit()
         return {"data":"Customer Updated"}