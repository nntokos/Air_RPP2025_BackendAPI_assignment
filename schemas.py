from pydantic import BaseModel
from typing import List, Optional

class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class CustomerOut(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class ShopItemCategoryBase(BaseModel):
    name: str

class ShopItemCategoryCreate(ShopItemCategoryBase):
    pass

class ShopItemCategoryUpdate(BaseModel):
    name: Optional[str] = None

class ShopItemCategoryOut(ShopItemCategoryBase):
    id: int
    class Config:
        orm_mode = True

class ShopItemBase(BaseModel):
    name: str
    price: float
    category_id: int

class ShopItemCreate(ShopItemBase):
    pass

class ShopItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class ShopItemOut(ShopItemBase):
    id: int
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None

class OrderOut(OrderBase):
    id: int
    class Config:
        orm_mode = True
