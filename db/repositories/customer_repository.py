from db.database import get_db
from db.models import Customer
from utils.hashing import Hashing

class CustomerRepository:
    def __init__(self):
        self.db=next(get_db())
    
    def get_customer(self,id:int):
        return self.db.query(Customer).filter(Customer.id==id).first()
    
    def get_customers(self,skip=0,limit=100):
        return self.db.query(Customer).offset(skip).limit(limit).all()
    
    def create_customer(self,Name,Passcode):
        hashObj=Hashing()
        hashed_Passcode=hashObj.hash(Passcode)
        db_cust=Customer(Name=Name,Passcode=hashed_Passcode)
        self.db.add(db_cust)
        self.db.commit()
        self.db.refresh(db_cust)
        return db_cust
    
    def update_customer(self,id,name):
        cust_record=self.db.query(Customer).filter(Customer.id==id).filter().first()
        if cust_record:
            cust_record.Name=name
            self.db.commit()
            self.db.refresh(cust_record)

    def delete_customer(self,id):
        cust_record=self.db.query(Customer).filter(Customer.id==id).filter().first()
        if cust_record:
            self.db.delete(cust_record)
            self.db.commit()