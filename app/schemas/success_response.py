from pydantic import BaseModel, model_serializer
from typing import Generic, TypeVar, Optional

# Define a generic type variable for the response data
T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    code: str = "SUCCESS"
    message: str = "Response fetched successfully."
    data: Optional[T] = None

    @model_serializer
    def ser_model(self):
        if not self.data:
            return {k: v for k, v in self.__dict__.items() if v is not None}
        return self.__dict__
