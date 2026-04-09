from fastapi import APIRouter, UploadFile, File, Body
from app.api.file_handler import file_handler
from app.api.task_manager import task_manager
from app.api.company_profile import company_profile_generator
from app.api.customer_strategy import customer_strategy_generator
from app.api.customer_search import customer_searcher, CustomerSearchInput
import os
from app.config.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "服务运行正常"}

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """上传 PDF 文件并处理"""
    # 保存文件
    file_id = await file_handler.save_uploaded_file(file)
    
    # 上传到 OpenAI
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.pdf")
    openai_file = file_handler.upload_to_openai(file_path)
    
    # 创建任务记录
    task = task_manager.create_task(file_id, file.filename, openai_file["id"])
    
    # 更新任务状态为完成
    task_manager.update_task_status(file_id, "completed", "文件处理完成")
    
    return {
        "success": True,
        "file_id": file_id,
        "openai_file_id": openai_file["id"],
        "filename": file.filename,
        "status": "completed"
    }

@router.get("/file/{file_id}")
async def get_file_status(file_id: str):
    """获取文件处理状态"""
    task = task_manager.get_task(file_id)
    if not task:
        return {"error": "文件不存在"}
    
    return {
        "file_id": task["file_id"],
        "filename": task["filename"],
        "status": task["status"],
        "message": task.get("message", ""),
        "created_at": task["created_at"].isoformat() if hasattr(task["created_at"], "isoformat") else str(task["created_at"]),
        "updated_at": task["updated_at"].isoformat() if hasattr(task["updated_at"], "isoformat") else str(task["updated_at"])
    }

@router.get("/tasks")
async def list_tasks():
    """列出所有任务"""
    tasks = task_manager.list_tasks()
    # 格式化时间
    for task in tasks:
        if hasattr(task.get("created_at"), "isoformat"):
            task["created_at"] = task["created_at"].isoformat()
        if hasattr(task.get("updated_at"), "isoformat"):
            task["updated_at"] = task["updated_at"].isoformat()
    return tasks

@router.post("/generate-profile/{file_id}")
async def generate_company_profile(file_id: str):
    """从 PDF 文件生成公司画像"""
    try:
        # 生成公司画像
        profile = company_profile_generator.generate_company_profile(file_id)
        
        # 更新任务状态
        task_manager.update_task_status(file_id, "completed", "公司画像生成完成")
        
        return {
            "success": True,
            "file_id": file_id,
            "profile": profile
        }
    except Exception as e:
        # 更新任务状态为失败
        task_manager.update_task_status(file_id, "failed", f"生成公司画像失败: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/generate-strategy")
async def generate_customer_strategy(company_profile: dict = Body(...)):
    """基于公司画像生成客户策略"""
    try:
        # 生成客户策略
        strategy = customer_strategy_generator.generate_customer_strategy(company_profile)
        
        return {
            "success": True,
            "strategy": strategy
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/search-customers")
async def search_customers(keywords: list = Body(..., description="搜索关键词"), industry: str = Body(None, description="行业"), location: str = Body(None, description="位置"), company_size: str = Body(None, description="公司规模")):
    """搜索候选客户"""
    try:
        # 创建搜索输入
        search_input = CustomerSearchInput(
            keywords=keywords,
            industry=industry,
            location=location,
            company_size=company_size
        )
        
        # 执行搜索
        results = customer_searcher.search_customers(search_input)
        
        return {
            "success": True,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
