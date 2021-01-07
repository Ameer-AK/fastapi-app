from fastapi import FastAPI
from controllers import customer, address

app = FastAPI()

app.include_router(customer.router)
app.include_router(address.router)


@app.get('/')
def home():
    return "Hello"