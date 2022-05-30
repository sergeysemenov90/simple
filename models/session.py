import datetime
from dataclasses import dataclass
from uuid import UUID

from database.models import User


@dataclass
class Session:
    key: UUID
    user: User
    expires: datetime.datetime
