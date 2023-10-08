from fastapi import FastAPI
from data.routes import contacts, auth

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
#uvicorn main:app --reload
@app.get("/")
async def root():
    return {"message": "App RUN"}

