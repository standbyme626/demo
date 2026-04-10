from fastapi import APIRouter, UploadFile, File, Body
from app.api.file_handler import file_handler
from app.api.task_manager import task_manager
from app.api.company_profile import company_profile_generator
from app.api.customer_strategy import customer_strategy_generator
from app.api.customer_search import customer_searcher, CustomerSearchInput
from app.api.customer_grading import customer_grader
from app.api.action_suggestion import action_suggestion_generator
from app.api.feishu_service import feishu_service, field_mapping_manager
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

@router.post("/grade-customers")
async def grade_customers(customers: list = Body(..., description="候选客户列表"), company_profile: dict = Body(..., description="公司画像"), customer_strategy: dict = Body(..., description="客户策略")):
    """对候选客户进行分级"""
    try:
        # 执行客户分级
        graded_customers = customer_grader.grade_multiple_customers(customers, company_profile, customer_strategy)
        
        return {
            "success": True,
            "graded_customers": graded_customers,
            "count": len(graded_customers)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/generate-action-suggestions")
async def generate_action_suggestions(graded_customers: list = Body(..., description="已分级客户列表"), company_profile: dict = Body(..., description="公司画像"), customer_strategy: dict = Body(..., description="客户策略")):
    """生成下一步动作建议"""
    try:
        # 生成动作建议
        suggestions = action_suggestion_generator.generate_suggestions(graded_customers, company_profile, customer_strategy)
        
        return {
            "success": True,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/feishu/test-connection")
async def test_feishu_connection():
    """测试飞书连接"""
    try:
        result = feishu_service.test_connection()
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/feishu/fields")
async def get_feishu_fields():
    """获取飞书多维表字段列表"""
    try:
        fields = feishu_service.list_fields()
        if fields is not None:
            return {
                "success": True,
                "fields": fields
            }
        else:
            return {
                "success": False,
                "error": "获取字段列表失败"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/feishu/mapping")
async def get_field_mapping():
    """获取字段映射配置"""
    try:
        mapping = field_mapping_manager.get_all_mappings()
        return {
            "success": True,
            "mapping": mapping
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/feishu/mapping")
async def set_field_mapping(mapping: dict = Body(..., description="字段映射配置")):
    """设置字段映射"""
    try:
        for source_field, target_field in mapping.items():
            field_mapping_manager.set_mapping(source_field, target_field)
        return {
            "success": True,
            "message": "字段映射设置成功",
            "mapping": field_mapping_manager.get_all_mappings()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/feishu/add-record")
async def add_record_to_feishu(data: dict = Body(..., description="要写入的数据"), use_mapping: bool = Body(True, description="是否使用字段映射")):
    """向飞书多维表添加单条记录"""
    try:
        if use_mapping:
            mapped_data = field_mapping_manager.map_data(data)
        else:
            mapped_data = data
        
        result = feishu_service.add_record(mapped_data)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/feishu/add-records-batch")
async def add_records_batch_to_feishu(data_list: list = Body(..., description="要写入的数据列表"), use_mapping: bool = Body(True, description="是否使用字段映射")):
    """向飞书多维表批量添加记录"""
    try:
        if use_mapping:
            mapped_data_list = field_mapping_manager.map_data_batch(data_list)
        else:
            mapped_data_list = data_list
        
        result = feishu_service.add_records_batch(mapped_data_list)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
