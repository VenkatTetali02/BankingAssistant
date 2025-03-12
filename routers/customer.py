from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List
from db import models
from db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import and_,func
import schemas
from db.repositories.customer_repository import CustomerRepository

router=APIRouter(prefix="/customers",tags=['Customer'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_customer(request:schemas.CustomerRequest,db:Session=Depends(get_db)):
    cust_repository=CustomerRepository(db)
    ret_status,message=cust_repository.create_customer(request.Name,request.Passcode)
    if ret_status:
        return message
    raise HTTPException(status.HTTP_400_BAD_REQUEST,message)

@router.get("/",response_model=List[schemas.CustomerResponse])
def get_customers(db:Session=Depends(get_db)):
    cust_repository=CustomerRepository(db)
    customers=cust_repository.get_customers()
    return customers

@router.get("/{cust_id}",status_code=status.HTTP_200_OK,response_model=schemas.CustomerResponse,tags=["Customer"])
def get_customer(cust_id:int,response: Response,db:Session=Depends(get_db)):
    cust_repository=CustomerRepository(db)
    ret_status,message=cust_repository.get_customer(cust_id)

    if ret_status:
        return message
    
    raise HTTPException(status.HTTP_404_NOT_FOUND,message)

@router.put("/{cust_id}",status_code=status.HTTP_202_ACCEPTED)
def update_customer(cust_id,request:schemas.CustomerRequest,db:Session=Depends(get_db)):
     cust_repository=CustomerRepository(db)
     ret_status,message=cust_repository.update_customer(cust_id,request.Name,request.Passcode)
     if ret_status:
         return {"data":message}
     else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,message)

@router.delete("/{cust_id}",status_code=status.HTTP_200_OK)
def delete_customer(cust_id:int,db:Session=Depends(get_db)):
     cust_repository=CustomerRepository(db)
     ret_status,message=cust_repository.delete_customer(cust_id)
     if ret_status:
        return {"data":message}
     
     raise HTTPException(status.HTTP_404_NOT_FOUND,message)