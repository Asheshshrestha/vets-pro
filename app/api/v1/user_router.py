from fastapi import (
    APIRouter,
    Depends,
    Query,
    Request,
    Response,
    status,
)
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.success_response import SuccessResponse
from app.schemas.user import UserCreate, UserOut
from app.services.implementation.user_impl import UserImplementation
from app.services.interface.user_interface import UserInterface

router = APIRouter(prefix=f"/api/v1/user", tags=["User"])


def get_user_service(
    db: Session = Depends(get_db)
) -> UserInterface:
    return UserImplementation(db)


@router.post(
    "/sign-up", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate,
    user_service: UserInterface = Depends(get_user_service)
):
    user_data = user_service.create_user(user, None)
    return SuccessResponse(
        message="User created successfully.",
        data=UserOut.model_validate(user_data).model_dump(),
    )
