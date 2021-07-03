import datetime
from typing import Optional

from pymongo import MongoClient
from pydantic import BaseModel, Field
from bson import ObjectId

client = MongoClient("localhost", 27017)

db = client.test
collection = db["posts"]


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Posts(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    author: str
    test: str
    date: datetime.datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
