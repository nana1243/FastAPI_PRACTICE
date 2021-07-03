# 1.FAST API 임포트

from fastapi import FastAPI

import views

app = FastAPI()
app.include_router(views.router)