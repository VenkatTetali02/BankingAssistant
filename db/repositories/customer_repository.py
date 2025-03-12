from db.models import Customer
from utils.hashing import Hashing
from db.database import get_db

class CustomerRepository:
    def __init__(self,db=next(get_db())):
        self.db=db
    
    def get_customer(self,id:int):
        cust_record=self.db.query(Customer).filter(Customer.id==id).first()
        if cust_record:
            return True, cust_record
        
        return False,f'Customer {id} Not Found'
    
    def get_customers(self,skip=0,limit=100):
        return self.db.query(Customer).offset(skip).limit(limit).all()
    
    def create_customer(self,name,passcode):
        if not Passcode:
            return False , f'Passcode is a required Field'
        hashObj=Hashing()
        hashed_Passcode=hashObj.hash(passcode)
        db_cust=Customer(Name=name,Passcode=hashed_Passcode)
        self.db.add(db_cust)
        self.db.commit()
        self.db.refresh(db_cust)
        return True,db_cust
    
    def update_customer(self,id,name,passcode):
        cust_record=self.db.query(Customer).filter(Customer.id==id).first()
        if cust_record:
            cust_record.Name=name
            cust_record.Passcode=passcode
            self.db.commit()
            self.db.refresh(cust_record)
            return True,f'Customer {id} Successfully Updated'
        
        return False,f'Customer Record with {id} not found'

    def delete_customer(self,id):
        cust_record=self.db.query(Customer).filter(Customer.id==id).first()
        if cust_record:
            self.db.delete(cust_record)
            self.db.commit()
            return True,f'Deleted Customer with {id} Successfully'
        
        return False,f'Customer with {id} Not Found'