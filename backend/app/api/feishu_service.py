import requests
from typing import Optional, Dict, Any, List
from app.config.config import settings
from app.config.logging import logger
import time
import json

class FeishuBitableService:
    def __init__(self):
        self.app_id = settings.FEISHU_APP_ID
        self.app_secret = settings.FEISHU_APP_SECRET
        self.app_token = settings.FEISHU_BITABLE_APP_TOKEN
        self.table_id = settings.FEISHU_BITABLE_TABLE_ID
        self.tenant_access_token = None
        self.token_expire_time = 0
        
        self.tenant_access_token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        self.base_api_url = "https://open.feishu.cn/open-apis/bitable/v1"
    
    def get_tenant_access_token(self) -> Optional[str]:
        if self.tenant_access_token and time.time() < self.token_expire_time - 60:
            return self.tenant_access_token
        
        try:
            payload = {
                "app_id": self.app_id,
                "app_secret": self.app_secret
            }
            response = requests.post(self.tenant_access_token_url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                self.tenant_access_token = result.get("tenant_access_token")
                self.token_expire_time = time.time() + result.get("expire", 7200)
                logger.info("获取飞书 tenant_access_token 成功")
                return self.tenant_access_token
            else:
                logger.error(f"获取飞书 tenant_access_token 失败: {result}")
                return None
        except Exception as e:
            logger.error(f"获取飞书 tenant_access_token 异常: {str(e)}")
            return None
    
    def _get_headers(self) -> Dict[str, str]:
        token = self.get_tenant_access_token()
        if not token:
            raise Exception("无法获取飞书访问令牌")
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def list_fields(self) -> Optional[List[Dict[str, Any]]]:
        try:
            url = f"{self.base_api_url}/apps/{self.app_token}/tables/{self.table_id}/fields"
            headers = self._get_headers()
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                return result.get("data", {}).get("items", [])
            else:
                logger.error(f"获取多维表字段列表失败: {result}")
                return None
        except Exception as e:
            logger.error(f"获取多维表字段列表异常: {str(e)}")
            return None
    
    def add_record(self, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.base_api_url}/apps/{self.app_token}/tables/{self.table_id}/records"
            headers = self._get_headers()
            payload = {
                "fields": fields
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                logger.info("添加记录成功")
                return {
                    "success": True,
                    "record": result.get("data", {}).get("record", {})
                }
            else:
                logger.error(f"添加记录失败: {result}")
                return {
                    "success": False,
                    "error": result.get("msg", "未知错误")
                }
        except Exception as e:
            logger.error(f"添加记录异常: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_records_batch(self, records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.base_api_url}/apps/{self.app_token}/tables/{self.table_id}/records/batch_create"
            headers = self._get_headers()
            payload = {
                "records": [{"fields": record} for record in records]
            }
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                logger.info(f"批量添加记录成功，共 {len(records)} 条")
                return {
                    "success": True,
                    "records": result.get("data", {}).get("records", [])
                }
            else:
                logger.error(f"批量添加记录失败: {result}")
                return {
                    "success": False,
                    "error": result.get("msg", "未知错误")
                }
        except Exception as e:
            logger.error(f"批量添加记录异常: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self) -> Dict[str, Any]:
        try:
            token = self.get_tenant_access_token()
            if not token:
                return {
                    "success": False,
                    "error": "无法获取访问令牌"
                }
            
            fields = self.list_fields()
            if fields is not None:
                return {
                    "success": True,
                    "message": "连接成功",
                    "fields": fields
                }
            else:
                return {
                    "success": False,
                    "error": "无法获取多维表字段列表"
                }
        except Exception as e:
            logger.error(f"测试连接异常: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

class FieldMappingManager:
    def __init__(self):
        self.default_mapping = {
            "company_name": "公司名称",
            "website": "网站",
            "industry": "行业",
            "location": "位置",
            "company_size": "公司规模",
            "email": "邮箱",
            "phone": "电话",
            "grade": "评级",
            "score": "评分",
            "notes": "备注"
        }
        self.custom_mapping = {}
    
    def set_mapping(self, source_field: str, target_field: str) -> None:
        self.custom_mapping[source_field] = target_field
    
    def get_mapping(self, source_field: str) -> Optional[str]:
        if source_field in self.custom_mapping:
            return self.custom_mapping[source_field]
        return self.default_mapping.get(source_field)
    
    def get_all_mappings(self) -> Dict[str, str]:
        mapping = self.default_mapping.copy()
        mapping.update(self.custom_mapping)
        return mapping
    
    def map_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mapped_data = {}
        for source_field, value in data.items():
            target_field = self.get_mapping(source_field)
            if target_field:
                mapped_data[target_field] = value
        return mapped_data
    
    def map_data_batch(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.map_data(data) for data in data_list]

feishu_service = FeishuBitableService()
field_mapping_manager = FieldMappingManager()
