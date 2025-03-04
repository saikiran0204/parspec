from pydantic import BaseModel
from typing import List

class OrderRequest(BaseModel):
    user_id: str
    item_ids: List[str]
    total_amount: float