from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
from database import get_db
from dependencies import get_current_user
from models import Ticket, Customer
from schemas import TicketCreate, TicketUpdate, TicketResponse

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Customer can create ticket only for themselves
    if current_user.role == "Customer":

        customer = crud.get_customer_by_email(
            db,
            current_user.email
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer profile not found"
            )

        ticket.customer_id = customer.id

    customer = crud.get_customer(db, ticket.customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    new_ticket = Ticket(
        customer_id=ticket.customer_id,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        category=ticket.category,
        status="Open"
    )

    return crud.create_ticket(db, new_ticket)


@router.get(
    "/",
    response_model=list[TicketResponse]
)
def get_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Admin
    if current_user.role == "Admin":
        return crud.get_tickets(db)

    # Support Agent
    if current_user.role == "Support Agent":
        return crud.get_agent_tickets(
            db,
            current_user.id
        )

    # Customer
    customer = crud.get_customer_by_email(
        db,
        current_user.email
    )

    if not customer:
        return []

    return db.query(Ticket).filter(
        Ticket.customer_id == customer.id
    ).all()


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = crud.get_ticket(
        db,
        ticket_id
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if current_user.role == "Admin":
        return ticket

    if current_user.role == "Support Agent":

        if ticket.assigned_agent_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return ticket

    customer = crud.get_customer_by_email(
        db,
        current_user.email
    )

    if not customer or ticket.customer_id != customer.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return ticket


@router.put(
    "/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    db_ticket = crud.get_ticket(
        db,
        ticket_id
    )

    if not db_ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Closed ticket cannot be updated
    if db_ticket.status == "Closed":
        raise HTTPException(
            status_code=400,
            detail="Closed tickets cannot be updated"
        )

    update_data = ticket.model_dump(
        exclude_unset=True
    )

    # Only assigned Support Agent can change status
    if "status" in update_data:

        if current_user.role != "Support Agent":
            raise HTTPException(
                status_code=403,
                detail="Only assigned support agent can change status"
            )

        if db_ticket.assigned_agent_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Ticket is not assigned to you"
            )

    return crud.update_ticket(
        db,
        db_ticket,
        update_data
    )


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = crud.get_ticket(
        db,
        ticket_id
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can delete tickets"
        )

    crud.delete_ticket(
        db,
        ticket
    )

    return {
        "message": "Ticket deleted successfully"
    }