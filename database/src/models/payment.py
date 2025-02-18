from pydantic import BaseModel
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: str
    amount: int
    currency: str
    status: str
    timestamp: datetime
    sender_id: str
    receiver_id: str


class PaymentMethod(BaseModel):
    method_id: str
    type: str
    details: str
    user_id: str


class Merchant(BaseModel):
    merchant_id: str
    name: str
    category: str
    contact_info: str