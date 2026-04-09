from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 服务器配置
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # 环境配置
    ENVIRONMENT: str = "development"
    
    # 日志配置
    LOG_LEVEL: str = "info"
    
    # OpenAI 配置
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo"
    
    # 文件存储配置
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # 数据库配置
    MONGO_URI: Optional[str] = None
    
    # 飞书应用配置
    FEISHU_APP_ID: Optional[str] = None
    FEISHU_APP_SECRET: Optional[str] = None
    FEISHU_BITABLE_APP_TOKEN: Optional[str] = None
    FEISHU_BITABLE_TABLE_ID: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
