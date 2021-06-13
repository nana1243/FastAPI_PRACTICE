# 1.FAST API 임포트
from typing import Optional

from fastapi import FastAPI
from enum import Enum

from pydantic import BaseModel

import views

app = FastAPI() #2. FastAPI instance 생성성

app.include_router(views.router)