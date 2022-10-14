
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    Username: Optional[str] = None
    User_id: Optional[str] = None
    Search: Optional[str] = None
    Since: Optional[str] = None
    Until: Optional[str] = None
    Limit: Optional[int] = None
    TwitterSearch: bool = False
    Lowercase: bool = True
    Query: str = None
    Backoff_exponent: float = 3.0
    Min_wait_time: int = 0
    Bearer_token: str = None
    Guest_token: str = None
    deleted: list = None
