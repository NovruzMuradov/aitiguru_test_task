"""
Схемы Pydantic для заказов.
"""
from pydantic import BaseModel


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderCreateSchema(BaseModel):
    client_id: int
    items: list[OrderItemSchema]

    class Config:
        orm_mode = True


class OrderResponseSchema(BaseModel):
    id: int
    client_id: int
    items: list[OrderItemSchema]

    class Config:
        orm_mode = True
