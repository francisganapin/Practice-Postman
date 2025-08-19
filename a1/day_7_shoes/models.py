from sqlmodel import SQLModel,Field
from typing import Optional

class Shoes(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)