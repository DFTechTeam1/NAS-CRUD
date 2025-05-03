from pydantic import BaseModel


class ResponseDefault(BaseModel):
    success: bool = True
    message: str = None
    data: dict = None
