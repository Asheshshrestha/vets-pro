from abc import ABC, abstractmethod
from app.schemas.user import UserCreate
from typing import List, Optional, Any
from app.models.user import User

class UserInterface(ABC):
    @abstractmethod
    def create_user(
        self, user: UserCreate, role_service: None
    ) -> User:
        pass