from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
from database import get_db
from dependencies import admin_required
from models import Customer
from schemas import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    existing_customer = crud.get_customer_by_email(
        db,
        customer.email
    )

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )

    return crud.create_customer(db, new_customer)


@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return crud.get_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    customer = crud.get_customer(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    db_customer = crud.get_customer(db, customer_id)

    if not db_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    update_data = customer.model_dump(exclude_unset=True)

    # Check duplicate email
    if "email" in update_data:
        existing = crud.get_customer_by_email(
            db,
            update_data["email"]
        )

        if existing and existing.id != customer_id:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    return crud.update_customer(
        db,
        db_customer,
        update_data
    )


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    customer = crud.get_customer(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    crud.delete_customer(db, customer)

    return {
        "message": "Customer deleted successfully"
    }