from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from typing import Dict, Any
import openai
from app.config.config import settings

# 初始化 OpenAI 客户端
openai.api_key = settings.OPENAI_API_KEY

class FileHandler:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_uploaded_file(self, file: UploadFile) -> str:
        """保存上传的文件"""
        # 检查文件类型
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持 PDF 文件")
        
        # 检查文件大小
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="文件大小超过限制")
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.upload_dir, f"{file_id}.pdf")
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return file_id
    
    def upload_to_openai(self, file_path: str) -> Dict[str, Any]:
        """上传文件到 OpenAI"""
        try:
            with open(file_path, "rb") as f:
                response = openai.files.create(
                    file=f,
                    purpose="assistants"
                )
            return response.to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"上传到 OpenAI 失败: {str(e)}")
    
    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """获取文件信息"""
        try:
            response = openai.files.retrieve(file_id)
            return response.to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取文件信息失败: {str(e)}")

file_handler = FileHandler()