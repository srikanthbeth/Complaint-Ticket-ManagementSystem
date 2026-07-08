from fastapi import FastAPI

from database import Base, engine

from routers import auth
from routers import customers
from routers import tickets
from routers import assignments
from routers import reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Complaint & Ticket Management System")

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(tickets.router)
app.include_router(assignments.router)
app.include_router(reports.router)


@app.get("/")
def home():
    return {
        "message": "Complaint Ticket Management API Running"
    }