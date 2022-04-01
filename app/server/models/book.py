from typing import Optional
from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    id: int = Field(gt=-1)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=20)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=50,
                                       min_length=1, default='No Description')
    rating: Optional[int] = Field(gt=-1, lt=101, default=0) 

    class Config:
        schema_extra = {
            "example": {
                "id": "9",
                "title": "Professional editor",
                "author": "Bonnac",
                "description": "This is the description",
                "rating": 90
            }
        }


class UpdateBookModel(BaseModel):
    
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    rating: Optional[int]


class successresponse(BaseModel):
    message:Optional[str] =None
    

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}