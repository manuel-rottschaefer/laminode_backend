from pydantic import BaseModel
from typing import List
from datetime import datetime

class LamiNodeRelease(BaseModel):
    version: str
    obtain_url: str
    published_at: datetime
    changelog: List[str]
    is_mandatory: bool = False
