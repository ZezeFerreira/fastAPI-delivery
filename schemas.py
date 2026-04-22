from pydantic import BaseModel, EmailStr
from typing import List


# Schema para criação de usuário comum
class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


# Schema para criação de usuário administrador
class UserAdmin(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
         from_attributes = True


# Schema para autenticação (login)
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


# Schema para criação de pedidos
class OrderSchema(BaseModel):
    user_id: int

    class Config:
        from_attributes = True


# Schema para criação de itens do pedido
class OrderItemSchema(BaseModel):
    quantity: int
    flavor: str
    size: str
    unit_price: float
   
    class Config:
        from_attributes = True


# Schema de resposta para pedidos (inclui itens)
class OrderResponseSchema(BaseModel):
    id: int
    status: str
    price: float
    itens: List[OrderItemSchema]

    class Config:
        from_attributes = True
