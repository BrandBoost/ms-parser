from typing import List
from typing import Optional

from pydantic import BaseModel


class OrganizationSearchQuery(BaseModel):
    cities: List[str]
    categories: List[str]
    phones: Optional[bool] = False
    only_mobile_phones: Optional[bool] = False
    without_departments: Optional[bool] = False


class YandexApiOrganization(BaseModel):
    coordinates: List[float]
    address: str
    name: str
    categories: List[dict]
    phone: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
