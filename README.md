# Complaint & Ticket Management System

## Project Overview

The Complaint & Ticket Management System is a backend REST API built using **FastAPI**. It enables customers to raise complaints, administrators to manage customers and tickets, and support agents to resolve assigned tickets.

The project includes JWT Authentication, Role-Based Authorization, CRUD operations, ticket assignment, search functionality, pagination, and automated API testing.

---

# Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Passlib (bcrypt)
- Uvicorn
- Pytest

---

# Project Structure

```
complaint_ticket_management_system/
│
├── routers/
│   ├── auth.py
│   ├── customers.py
│   ├── tickets.py
│   ├── assignments.py
│   └── reports.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_customer.py
│   ├── test_ticket.py
│   ├── test_assignment.py
│   └── test_reports.py
│
├── auth.py
├── crud.py
├── database.py
├── dependencies.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
├── complaint.db
└── README.md
```

---

# Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing using bcrypt

---

## Roles

- Admin
- Support Agent
- Customer

---

## Customer Management

- Create Customer
- View Customers
- View Customer by ID
- Update Customer
- Delete Customer

---

## Ticket Management

- Create Ticket
- View Tickets
- View Ticket by ID
- Update Ticket
- Delete Ticket

---

## Ticket Assignment

- Assign Ticket to Support Agent
- View Tickets Assigned to Agent

---

## Reports

- Search Ticket by Title
- Filter by Priority
- Filter by Status
- View Customer Tickets
- Pagination

---

## Business Rules

- One customer can create multiple tickets.
- A ticket can be assigned to only one support agent.
- Closed tickets cannot be updated.
- Only assigned support agent can change ticket status.
- Admin can manage all modules.
- Customer can view only their own tickets.
- Support Agent can manage only assigned tickets.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/complaint_ticket_management_system.git
```

```bash
cd complaint_ticket_management_system
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
uvicorn main:app --reload
```

Application URL

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | /auth/register |
| POST | /auth/login |

---

## Customers

| Method | Endpoint |
|---------|----------|
| POST | /customers |
| GET | /customers |
| GET | /customers/{id} |
| PUT | /customers/{id} |
| DELETE | /customers/{id} |

---

## Tickets

| Method | Endpoint |
|---------|----------|
| POST | /tickets |
| GET | /tickets |
| GET | /tickets/{id} |
| PUT | /tickets/{id} |
| DELETE | /tickets/{id} |

---

## Assignment

| Method | Endpoint |
|---------|----------|
| POST | /tickets/{ticket_id}/assign/{agent_id} |
| GET | /agents/{agent_id}/tickets |

---

## Reports

| Method | Endpoint |
|---------|----------|
| GET | /reports/tickets |
| GET | /reports/customers/{customer_id}/tickets |

---

# Authentication

Protected APIs require JWT token.

Example Header

```
Authorization: Bearer <your_access_token>
```

---

# Running Tests

Execute all tests

```bash
pytest
```

Run with verbose output

```bash
pytest -v
```

---

# Sample Users

## Admin

```
Email:
admin@gmail.com

Password:
admin123
```

---

## Support Agent

```
Email:
agent@gmail.com

Password:
agent123
```

---

## Customer

```
Email:
customer@gmail.com

Password:
customer123
```

---

# Validation

- Unique Email
- Valid Phone Number
- JWT Authentication
- Role-Based Authorization
- Closed Tickets Cannot Be Updated
- Assigned Agent Only Can Update Ticket Status

---

# Future Enhancements

- Email Notifications
- File Attachments
- Ticket Comments
- Dashboard Analytics
- Docker Support
- PostgreSQL Deployment
- CI/CD Pipeline

---

# Author

**Srikanth Bethamcharla**

Backend Developer

---

# License

This project is developed for learning and educational purposes.
