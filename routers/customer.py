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
    cust_repository=CustomerRepository()
    new_customer=cust_repository.create_customer(request.Name,request.Passcode)
    return new_customer

@router.get("/",response_model=List[schemas.CustomerResponse])
def get_customers(db:Session=Depends(get_db)):
    customers=db.query(models.Customer).all()
    return customers

@router.get("/{cust_id}",status_code=status.HTTP_200_OK,response_model=schemas.CustomerResponse,tags=["Customer"])
def get_customer(cust_id:int,response: Response,db:Session=Depends(get_db)):
    customer=db.query(models.Customer).filter(models.Customer.id==cust_id).first()
    if not customer:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"No Customer with ID {cust_id}")
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"data":"No Customer with that ID exists"}
    return customer

@router.delete("/{cust_id}",status_code=status.HTTP_200_OK)
def delete_customer(cust_id:int,db:Session=Depends(get_db)):
     db.query(models.Customer).filter(models.Customer.id==cust_id).delete(synchronize_session=False)
     db.commit()
     return {"data":f"ID {cust_id} deleted"}

@router.put("/{cust_id}",status_code=status.HTTP_202_ACCEPTED)
def update_customer(cust_id,request:schemas.CustomerRequest,db:Session=Depends(get_db)):
     customer=db.query(models.Customer).filter(models.Customer.id==cust_id)
     if not customer.first():
         raise HTTPException(status.HTTP_404_NOT_FOUND,f"Customer with ID {cust_id} not found")
     else:
         customer.update({"Name":request.Name,"Pin":request.Pin})
         db.commit()
         return "Customer Updated"
         #customer.Name=request.Name
         #customer.Pin=request.Pin
         #db.refresh(customer)
         # eturn {"data":f"Updated CustID {cust_id}"}