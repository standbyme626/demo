from pymongo import MongoClient
from typing import Optional, Dict, Any
from app.config.config import settings
import datetime

class TaskManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.tasks = None
        self._initialize_db()
    
    def _initialize_db(self):
        """初始化数据库连接"""
        if settings.MONGO_URI:
            try:
                self.client = MongoClient(settings.MONGO_URI)
                self.db = self.client.get_database("pdf_parser")
                self.tasks = self.db.get_collection("tasks")
            except Exception as e:
                print(f"数据库连接失败: {str(e)}")
                # 回退到内存存储
                self.tasks = {}
        else:
            # 使用内存存储作为回退
            self.tasks = {}
    
    def create_task(self, file_id: str, filename: str, openai_file_id: str) -> Dict[str, Any]:
        """创建任务记录"""
        task_data = {
            "file_id": file_id,
            "filename": filename,
            "openai_file_id": openai_file_id,
            "status": "processing",
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        }
        
        if isinstance(self.tasks, dict):
            self.tasks[file_id] = task_data
        else:
            self.tasks.insert_one(task_data)
        
        return task_data
    
    def update_task_status(self, file_id: str, status: str, message: Optional[str] = None) -> Dict[str, Any]:
        """更新任务状态"""
        update_data = {
            "status": status,
            "updated_at": datetime.datetime.utcnow()
        }
        
        if message:
            update_data["message"] = message
        
        if isinstance(self.tasks, dict):
            if file_id in self.tasks:
                self.tasks[file_id].update(update_data)
                return self.tasks[file_id]
            else:
                return None
        else:
            result = self.tasks.update_one(
                {"file_id": file_id},
                {"$set": update_data}
            )
            if result.matched_count > 0:
                return self.get_task(file_id)
            else:
                return None
    
    def get_task(self, file_id: str) -> Optional[Dict[str, Any]]:
        """获取任务信息"""
        if isinstance(self.tasks, dict):
            return self.tasks.get(file_id)
        else:
            return self.tasks.find_one({"file_id": file_id})

    def list_tasks(self) -> list:
        """列出所有任务"""
        if isinstance(self.tasks, dict):
            return list(self.tasks.values())
        else:
            return list(self.tasks.find())

task_manager = TaskManager()