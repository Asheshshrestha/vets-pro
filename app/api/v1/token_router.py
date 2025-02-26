from fastapi import(
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.success_response import SuccessResponse
from app.schemas.token import RefreshTokenRequest, UserAuth
from app.services.implementation.token_impl import TokenImplementation
from app.services.interface.token_interface import TokenInterface

router = APIRouter(prefix=f"/api/v1/token",tags=["Token"])

def get_token_service(
        db:Session = Depends(get_db)
) -> TokenInterface:
    return TokenImplementation(db)

@router.post(
    "/grant",response_model= SuccessResponse,status_code=status.HTTP_200_OK
)
def grant_token(
    user: UserAuth,
    token_service: TokenInterface = Depends(get_token_service)
):
    token = token_service.grant_token(user=user)
    return SuccessResponse(
        message="Token generated successfully",
        data= token.model_dump()
    )

@router.post(
    "/refresh",response_model= SuccessResponse,status_code=status.HTTP_200_OK
)
def refresh_token(
    refresh_token: RefreshTokenRequest,
    token_service: TokenInterface = Depends(get_token_service)
):
    token = token_service.refresh_access_token(refresh_token=refresh_token.refresh_token)
    return SuccessResponse(
        message="Token generated successfully",
        data= token.model_dump()
    )