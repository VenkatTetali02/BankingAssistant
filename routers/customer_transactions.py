from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List
from db.database import get_db
from sqlalchemy.orm import Session
import schemas
from db.repositories.customer_transaction_repository import CustomerTransactionRepository

router=APIRouter(prefix="/customers/transactions",tags=['CustomerTransactions'])

@router.post("/")
def create_customer_transactions(request:schemas.CustomerTransactionRequest,db:Session=Depends(get_db)):
    cust_tran_repo=CustomerTransactionRepository(db)
    ret_status,message=cust_tran_repo.create_customer_transaction(request.AccountNum,request.Amount,request.Description)
    if ret_status:
        return message
    else:
        raise HTTPException(status.HTTP_409_CONFLICT,message)

@router.get("/{cust_id}/{acct_type}/{lastN}")
def get_last_n_transactions(cust_id,acct_type,lastN=5,db:Session=Depends(get_db)):
    cust_tran_repo=CustomerTransactionRepository(db)
    result=cust_tran_repo.get_last_n_customer_transactions(cust_id,acct_type,lastN)
    return {"data":result}