from fastapi import FastAPI
from db import models
from db.database import engine
from routers import customer,bot, customer_accounts
from fastapi import APIRouter, status, Depends, HTTPException, Response, Request

models.Base.metadata.create_all(bind=engine)
#models.Base.metadata.drop_all(bind=engine)

app=FastAPI()
app.include_router(customer.router)
app.include_router(customer_accounts.router)
app.include_router(bot.router)

@app.get("/")
def homepage():
    return "Welcome to Bank API Portal"

@app.post("/")
def bot_response(request:Request):
    print(request)
    return {"fullfillmentText":"Received the request"}

