from pydantic import BaseModel
from typing import List

# Objects Schemas used during creation
class CustomerRequest(BaseModel):
    Name:str
    Passcode:str

class CustomerAccountRequest(BaseModel):
    AccountType:str
    Balance:float
    CustID:int

class CustomerAccountUpdateRequest(BaseModel):
    AccountType:str
    Balance:float

class CustomerTransactionRequest(BaseModel):
     AccountNum: int
     Amount: float
     Description: str


# Schemas used in the middle to avoid repetetion
class CustomerAccountObj(BaseModel):
    AccountType:str
    CustID:int
    AccountNum:int

# Objects schemas used during Return time
class CustomerResponse(BaseModel):
    Name:str
    class Config:
        from_attributes=True


class CustomerAccountResponse(BaseModel):
    AccountType:str
    CustID:int
    owner:CustomerResponse
    class Config:
        from_attributes=True
