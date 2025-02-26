from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from app.services.interface.token_interface import TokenInterface
from app.schemas.token import RefreshTokenRequest, TokenResponse, UserAuth
from app.models.user import User 
from app.utils.password_utils import verify_password
from app.config.logger import logger
from app.exceptions.custom_exception import (NotFoundException,BadRequestException)
# Constants
SECRET_KEY = "474d44201d339d03fb9e4710d18c7d993b6cb3ce7bf0824a87d98dbe2dbedc4926dac163f5775218d3d9a24866e087f2682ebd3b4720092aa6791c6801e5decbd7548cdc5f94bb213e9cd7bb673eba172f4d65cdb4a6566f205e86f59991899e55c70b55d85492a060e8bc19a27dd746677646ffa014618a5d9c84736f15c8599786a5fd1e5e4aa88ab4149cc1e85490ff3430f154916e39e8f03a74df770f700882729579f1e7f0ee03ab3a3772886fd8eb6edfa3b07f03a78aa7df5d7f48bd74567378ec1c022addbe322d4bb90ba6a98ea9e508acc86c4c463a60c52d0c2253768110c8a0b57f8b90905d8fac4e7dfb21239c9f519719b62df12eb800b634"
REFRESH_SECRET_KEY = "8826831355d46923c990542d69ccfd5ac197c2ed7f7d080e2087ae4c5a2fe210f3f83eab2abeebeba16bca635d13c4727b988d683b6a67023587230380934eb3be938e5285825717acb6adbc71994b5ae07b54f4db014acb46d567fd90aeb34dc16f7c1aa66e85d7187b8de61703e677a1184939bb05ffb5c3778aef5f46129dd29580c739b902ca7b93b63d59c530107cec1e9f763d1ab7996c01414db67ef24fa1f6cc75c511211af4dee02aaec657ec578395c1a0748c0b47ec7d454929a9d330fa09aab23cedf1f69f3404c4316a586262ccb30e092b3c49e11b4f96bb54a9b4ab924c2fe453b74056a72f022f5cb7dc58394c8a624a9c9e210aadfdc1cc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class TokenImplementation(TokenInterface):
    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def authenticate_user(self, username: str, password: str):
        """Authenticate the user by checking the credentials in the database."""
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password):
            return None
        return user

    def create_token(self, data: dict, expires_delta: timedelta, secret_key: str):
        """Generate a JWT token with an expiration time."""
        to_encode = data.copy()
        expire = datetime.now()+ expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

    def grant_token(self, user: UserAuth):
        """Authenticate the user and return access & refresh tokens."""
        authenticated_user = self.authenticate_user(user.username, user.password)
        if not authenticated_user:
            raise BadRequestException(message="Invalid username or password")

        access_token = self.create_token(
            data={"sub": authenticated_user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            secret_key=SECRET_KEY
        )

        refresh_token = self.create_token(
            data={"sub": authenticated_user.username},
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            secret_key=REFRESH_SECRET_KEY
        )
        token = TokenResponse(
            access_token=access_token,
            refresh_token= refresh_token,
        )
        return token

    def refresh_access_token(self, refresh_token: str):
        """Validate refresh token and generate a new access token."""
        try:
            payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise BadRequestException(message="Invalid refresh token")

            # Generate a new access token
            new_access_token = self.create_token(
                data={"sub": username},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                secret_key=SECRET_KEY
            )
            token = TokenResponse(
            access_token=new_access_token,
            refresh_token= None
            )
            return token

        except jwt.JWTError:
            raise BadRequestException(message="Invalid refresh token")