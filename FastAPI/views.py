from typing import List, Optional

from fastapi import APIRouter, Query, Path, Depends, Request
from fastapi.security import APIKeyHeader
from fastapi.security.http import HTTPBase

from constants import ModelName
from models import Item, db, Posts

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


# @router.get("/items/{item_id}")
# async def read_item(item_id : int):
#     return {"item_id" : item_id}


# 경로 동작은 순차적으로 평가된다.

@router.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@router.get("/files/{file_path:path}")
async def get_files(file_path: str):
    return {"file_path": file_path}


# 쿼리 매개 변수
# @router.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# 선택적 매개변수

# @router.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

# Request Body


@router.post("/items/")
async def create_item(item: Item):
    return item


# Declare it as a parameter

# @router.put("/items/{item_id}")
# async def create_item(item_id:int, item :Item):
#     return {item_id: item_id, **item.dict()}


# Query Parameters and String Validations

@router.get("/items/")
# async def read_items(q:Optional[str] = None):
#     results = {
#         "items": [{"1": "Foo"}, {"2" :"Boo"}]
#     }
#
#     if q:
#         results.update({"q":q})
#     return results

@router.get("/items/")
async def read_items(q: List[str] = Query(["test1", "test2"])):
    query_items = {"q": q}
    return query_items


# @router.get("/items/{item_id}")
# async def read_items(
#     *, item_id: int = Path(..., title="The ID of the item to get"), q: str
#
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results


# Number validations: greater than or equal¶

@router.get("/items/{item_id}")
async def read_items(
        *, item_id: int = Path(..., title="The ID of the item to get", ge=1, le=1000), q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@router.get('/posts')
async def list_posts():
    posts = []
    for post in db.users.find():
        posts.append(Posts(**post))
    return {'posts': posts}


class APIKeyEnterprise(APIKeyHeader):
    def __init__(self):
        super().__init__(name="ViodioAK")
        print()

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = await super().__call__(request)
        print('this is apikey!')
        print(api_key)
        return api_key


def current_enterprise(api_key: str = Depends(APIKeyEnterprise())) -> bool:
    print(api_key, "test!")
    return True


class APIKeyEnterprise2(HTTPBase):
    def __init__(self):
        super().__init__(scheme="ViodioAK")

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = await super().__call__(request)
        print("!!!!!")
        print(api_key.scheme)
        return api_key


def current_enterprise2(api_key: str = Depends(APIKeyEnterprise2())):
    return True



@router.get("/items/{item_id}")
def read_item(item_id: int, test=Depends(current_enterprise), q: Optional[str] = None):
    print("test is : ", test)
    return {"item_id": item_id, "q": q}


@router.get("/items")
def read_item(test=Depends(current_enterprise2), q: Optional[str] = None):
    print("test is : ", test)
    return {"test": ["teset1", "test2"]}
