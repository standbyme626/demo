from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import settings
from app.config.logging import logger
from app.config.exception_handler import global_exception_handler, http_exception_handler

app = FastAPI(
    title="外贸获客智能体 API",
    description="提供外贸获客相关的API服务",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

from app.api import routes

app.include_router(routes.router)

logger.info("应用初始化完成")
