from app.exceptions.custom_exception import CustomException, NotFoundException
from app.models.user import User,UserProfile
from app.schemas.user import UserCreate
from app.services.interface.user_interface import UserInterface
from app.services.validator.user_validator import (validate_password,
                                                   validate_new_user,
                                                   validate_username)
from app.utils.password_utils import hash_password
from sqlalchemy.orm import Session
from app.config.logger import logger
class UserImplementation(UserInterface):
    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def get_user_by_id(self,user_id: int) -> User:
        try:
            user = (
                self.db.query(User)
                .filter(User.id == user_id,User.is_active.is_(True))
                .first()
            )
            if not user:
                logger.info("User not found")
                raise NotFoundException(message="User not found")
        except Exception as e:
            logger.info("Error on fetching user by ID")
            raise CustomException(message="Error on fetching user by ID")
    def create_user(
        self, user: UserCreate, role_service: None
    ) -> User:
        validate_username(user.username)
        validate_password(user.password)
        validate_new_user(self.db,user.username)
        hashed_password = hash_password(user.password)
        try:
            new_user = User(
                username = user.username,
                password = hashed_password
            )
            self.db.add(new_user)
            self.db.flush()
        except CustomException:
            raise
        
        except Exception as e:
            self.db.rollback()
            logger.info(f"Error on adding new user:{e}")
            raise CustomException(message="Error on adding new user")
        
        try:
            new_profile = UserProfile(
                user_id = new_user.id
            )
            self.db.add(new_profile)
            self.db.commit()
            self.db.refresh(new_user)
            self.db.refresh(new_profile)
        except CustomException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.info(f"Error on adding new user's profile: {e}")
            raise CustomException(message="Error on adding new user's profile")
        
        return new_user