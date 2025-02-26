from abc import ABC, abstractmethod
from app.schemas.token import TokenResponse, UserAuth,RefreshTokenRequest

class TokenInterface(ABC):

    @abstractmethod
    def grant_token(
        self,
        user: UserAuth
    ) -> TokenResponse:
        pass

    @abstractmethod
    def refresh_access_token(
        self,
        refresh_token: str
    ) -> TokenResponse:
        pass