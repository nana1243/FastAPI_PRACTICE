from typing import List, Optional

import jwt as jwt
from fastapi import APIRouter, Query, Path, Depends, Request
from fastapi.security import APIKeyHeader
from fastapi.security.http import HTTPBase
from pydantic import BaseModel

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


class JWTClaims(BaseModel):
    typ: str = "JWT"
    alg: str = "HS256"
    jti: str
    sub: Optional[str] = None
    iss: str = "viodio"
    iat: int
    exp: int
    token_type: str


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
        credentials = await super().__call__(request)
        print(credentials and credentials.credentials)
        return credentials and credentials.credentials

def decode_jwt(token: Optional[str] = None, auto_error: bool = True) -> Optional[JWTClaims]:
    if token is None:
        if auto_error:
            raise ValueError("check1")
        return None
    print(token.encode())
    claims = jwt.decode(token.encode(), key="12928")
    print("this is claims!")
    print(claims)

    # try:
    #     claims.validate(now=int(datetime.datetime.utcnow().timestamp()))
    # except (jose_errors.ExpiredTokenError, jose_errors.InvalidClaimError) as exc:
    #     raise HTTPException(
    #         status_code=http.HTTPStatus.UNAUTHORIZED,
    #         detail=jsonable_encoder(
    #             base_schema.ErrorResponse(title=str(exc), type=exceptions.ErrorType.UNAUTHORIZED)
    #         ),
    #         headers={"WWW-Authenticate": AUTH_SCHEME},
    #     )
    # return JWTClaims(**claims)

def get_current_enterprise_user(token: str):
    claims = decode_jwt(token)  # 이거 그대로 쓰면 안됨
    return True



def current_enterprise2(api_key: str = Depends(APIKeyEnterprise2())):
    return get_current_enterprise_user(api_key)


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, test=Depends(current_enterprise), q: Optional[str] = None):
    print("test is : ", test)
    return {"item_id": item_id, "q": q}


@router.get("/items")
def read_item(test=Depends(current_enterprise2), q: Optional[str] = None):
    print("test is : ", test)
    return {"test" : ["teset1","test2"]}
