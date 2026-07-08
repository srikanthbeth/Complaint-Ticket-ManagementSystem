from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal


# ==========================
# User Schemas
# ==========================

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["Admin", "Support Agent", "Customer"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================
# Customer Schemas
# ==========================

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(
        ...,
        pattern=r"^[6-9]\d{9}$"
    )
    address: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^[6-9]\d{9}$"
    )
    address: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True


# ==========================
# Ticket Schemas
# ==========================

class TicketBase(BaseModel):
    customer_id: int
    title: str
    description: str
    priority: Literal["Low", "Medium", "High"]
    category: str


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal["Low", "Medium", "High"]] = None
    category: Optional[str] = None
    status: Optional[
        Literal["Open", "In Progress", "Resolved", "Closed"]
    ] = None


class TicketResponse(BaseModel):
    id: int
    customer_id: int
    assigned_agent_id: Optional[int] = None
    title: str
    description: str
    priority: Literal["Low", "Medium", "High"]
    category: str
    status: Literal["Open", "In Progress", "Resolved", "Closed"]

    class Config:
        from_attributes = True