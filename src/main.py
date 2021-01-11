from fastapi import FastAPI

from controllers import address, customer

app = FastAPI()

app.include_router(customer.router)
app.include_router(address.router)


@app.get('/')
def home():
    return "Hello"
