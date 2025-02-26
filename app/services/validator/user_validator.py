import re
from app.exceptions.custom_exception import BadRequestException
from sqlalchemy.orm import Session

from app.models.user import User

@staticmethod
def validate_password(password: str) -> None:
    if len(password) < 8:
        raise BadRequestException(
            message="Password must be at least 8 characters long."
        )
    if not re.search(r"[A-Z]", password):
        raise BadRequestException(
            message="Password must contain at least one uppercase letter."
        )
    if not re.search(r"[a-z]", password):
        raise BadRequestException(
            detail="Password must contain at least one lowercase letter."
        )
    if not re.search(r"\d", password):
        raise BadRequestException(
            message="Password must contain at least one digit."
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise BadRequestException(
            message="Password must contain at least one special character."
        )
    

@staticmethod
def validate_username(username: str) -> None:
    # Regex pattern to validate email format
    pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    if not pattern.match(username):
        raise BadRequestException(message="Invalid email format.")
    

@staticmethod
def validate_new_user(db: Session,username: str) -> None:
    user = db.query(User).filter(
        User.is_active.is_(True),
        User.username == username
    ).first()
    if user:
        raise BadRequestException(
            message=f"User with email {username} already exist"
        )
