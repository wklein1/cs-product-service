from models.custom_base_model import CustomBaseModel
from pydantic import Field

class ProductsModel(CustomBaseModel):
    key: str = Field(alias="productId")
    owner_id: str
    name: str
    description: str
    component_ids: list[str]
    price: float