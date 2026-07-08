from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
from database import get_db
from dependencies import admin_required
from models import User

router = APIRouter(
    tags=["Ticket Assignment"]
)


@router.post("/tickets/{ticket_id}/assign/{agent_id}")
def assign_ticket(
    ticket_id: int,
    agent_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    ticket = crud.get_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    agent = crud.get_user_by_id(db, agent_id)

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support Agent not found"
        )

    if agent.role != "Support Agent":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected user is not a Support Agent"
        )

    ticket = crud.assign_ticket(
        db,
        ticket,
        agent
    )

    return {
        "message": "Ticket assigned successfully",
        "ticket": ticket
    }


@router.get("/agents/{agent_id}/tickets")
def get_agent_tickets(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    agent = crud.get_user_by_id(db, agent_id)

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support Agent not found"
        )

    if agent.role != "Support Agent":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a Support Agent"
        )

    return crud.get_agent_tickets(
        db,
        agent_id
    )