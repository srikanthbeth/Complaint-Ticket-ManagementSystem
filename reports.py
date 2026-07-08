from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Ticket
from dependencies import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/tickets")
def search_tickets(
    title: str = None,
    priority: str = None,
    status: str = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    query = db.query(Ticket)

    if title:
        query = query.filter(Ticket.title.contains(title))

    if priority:
        query = query.filter(Ticket.priority == priority)

    if status:
        query = query.filter(Ticket.status == status)

    total = query.count()

    tickets = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "tickets": tickets
    }


@router.get("/customers/{customer_id}/tickets")
def customer_tickets(
    customer_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    tickets = db.query(Ticket).filter(
        Ticket.customer_id == customer_id
    ).all()

    return tickets