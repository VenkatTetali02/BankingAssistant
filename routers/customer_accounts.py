from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List
from db import models
from db.database import get_db
from sqlalchemy.orm import Session
import schemas
from db.repositories.customer_accounts_repository import CustomerAccountRepository

router=APIRouter(prefix="/customer/accounts",tags=['CustomerAccounts'])

@router.post("/")
def create_customer_accounts(request:schemas.CustomerAccountRequest,db:Session=Depends(get_db)):
    cust_account_repo=CustomerAccountRepository(db)
    ret_status,message=cust_account_repo.create_customer_account(request.CustID,request.AccountType,request.Balance)
    if ret_status:
        return message
    else:
        raise HTTPException(status.HTTP_409_CONFLICT,message)

@router.get("/",response_model=List[schemas.CustomerAccountResponse])
def get_all_customer_accounts(db:Session=Depends(get_db)):
   cust_account_repo=CustomerAccountRepository(db)
   accounts=cust_account_repo.get_all_customer_accounts()
   return accounts

@router.get("/{cust_id}",response_model=List[schemas.CustomerAccountResponse])
def get_customer_account(cust_id,db:Session=Depends(get_db)):
   cust_account_repo=CustomerAccountRepository(db)
   ret_status,message=cust_account_repo.get_customer_accounts(cust_id)
   if ret_status:
       return message
   raise HTTPException(status.HTTP_404_NOT_FOUND,message)

@router.put("/{cust_id}")
def update_customer_accounts(cust_id,request:schemas.CustomerAccountUpdateRequest,db:Session=Depends(get_db)):
   cust_account_repo=CustomerAccountRepository(db)
   status,message=cust_account_repo.update_customer_account(cust_id,request.AccountType,request.Balance)
   # cust_account=db.query(models.CustomerAccount).filter(models.CustomerAccount.CustID==cust_id and models.CustomerAccount.AccountType==request.AccountType and models.CustomerAccount.AccountNum==request.AccountNum)
   if status:
          return {"data":message}
   else:
         raise HTTPException(status.HTTP_404_NOT_FOUND,message)
        