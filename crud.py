from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import User, Customer, Ticket


# =====================================================
# USER CRUD
# =====================================================

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.email == email
    ).first()


def get_all_users(db: Session):
    return db.query(User).all()


# =====================================================
# CUSTOMER CRUD
# =====================================================

def create_customer(db: Session, customer: Customer):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(
        Customer.id == customer_id
    ).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(
        Customer.email == email
    ).first()


def get_customers(db: Session):
    return db.query(Customer).all()


def update_customer(
    db: Session,
    db_customer: Customer,
    update_data: dict
):
    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)

    return db_customer


def delete_customer(
    db: Session,
    customer: Customer
):
    db.delete(customer)
    db.commit()


# =====================================================
# TICKET CRUD
# =====================================================

def create_ticket(
    db: Session,
    ticket: Ticket
):
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_ticket(
    db: Session,
    ticket_id: int
):
    return db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()


def get_tickets(db: Session):
    return db.query(Ticket).all()


def update_ticket(
    db: Session,
    db_ticket: Ticket,
    update_data: dict
):
    for key, value in update_data.items():
        setattr(db_ticket, key, value)

    db.commit()
    db.refresh(db_ticket)

    return db_ticket


def delete_ticket(
    db: Session,
    ticket: Ticket
):
    db.delete(ticket)
    db.commit()


# =====================================================
# ASSIGNMENT CRUD
# =====================================================

def assign_ticket(
    db: Session,
    ticket: Ticket,
    agent: User
):
    ticket.assigned_agent_id = agent.id

    db.commit()
    db.refresh(ticket)

    return ticket


def get_agent_tickets(
    db: Session,
    agent_id: int
):
    return db.query(Ticket).filter(
        Ticket.assigned_agent_id == agent_id
    ).all()


# =====================================================
# REPORTS
# =====================================================

def search_tickets(
    db: Session,
    title: str = None,
    priority: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10
):

    query = db.query(Ticket)

    if title:
        query = query.filter(
            Ticket.title.ilike(f"%{title}%")
        )

    if priority:
        query = query.filter(
            Ticket.priority == priority
        )

    if status:
        query = query.filter(
            Ticket.status == status
        )

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()


def get_customer_tickets(
    db: Session,
    customer_id: int
):
    return db.query(Ticket).filter(
        Ticket.customer_id == customer_id
    ).all()


def get_open_tickets(db: Session):
    return db.query(Ticket).filter(
        Ticket.status == "Open"
    ).all()


def get_closed_tickets(db: Session):
    return db.query(Ticket).filter(
        Ticket.status == "Closed"
    ).all()


def get_high_priority_tickets(db: Session):
    return db.query(Ticket).filter(
        Ticket.priority == "High"
    ).all()


def get_unassigned_tickets(db: Session):
    return db.query(Ticket).filter(
        Ticket.assigned_agent_id == None
    ).all()