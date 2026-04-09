from typing import Dict, Any, List, Optional
import openai
from app.config.config import settings

# 初始化 OpenAI 客户端
openai.api_key = settings.OPENAI_API_KEY

# 公司画像 JSON Schema
company_profile_schema = {
    "type": "object",
    "properties": {
        "company_name": {
            "type": "string",
            "description": "公司名称"
        },
        "industry": {
            "type": "string",
            "description": "所属行业"
        },
        "location": {
            "type": "string",
            "description": "公司所在地"
        },
        "established_year": {
            "type": "string",
            "description": "成立年份"
        },
        "business_model": {
            "type": "string",
            "description": "商业模式"
        },
        "products_services": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "产品和服务"
        },
        "target_markets": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "目标市场"
        },
        "competitors": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "竞争对手"
        },
        "key_clients": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "主要客户"
        },
        "revenue": {
            "type": "string",
            "description": "年收入"
        },
        "employee_count": {
            "type": "string",
            "description": "员工数量"
        },
        "contact_info": {
            "type": "object",
            "properties": {
                "website": {
                    "type": "string",
                    "description": "公司网站"
                },
                "email": {
                    "type": "string",
                    "description": "联系邮箱"
                },
                "phone": {
                    "type": "string",
                    "description": "联系电话"
                },
                "address": {
                    "type": "string",
                    "description": "公司地址"
                }
            },
            "description": "联系信息"
        },
        "key_strengths": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "核心优势"
        },
        "growth_potential": {
            "type": "string",
            "description": "增长潜力"
        },
        "risk_factors": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "风险因素"
        },
        "notes": {
            "type": "string",
            "description": "其他备注"
        }
    },
    "required": ["company_name"]
}

class CompanyProfileGenerator:
    def __init__(self):
        pass
    
    def generate_company_profile(self, file_id: str) -> Dict[str, Any]:
        """从 PDF 文件生成公司画像"""
        try:
            # 构建 prompt
            prompt = "你是一个专业的外贸获客分析师，请从以下 PDF 文件中提取信息，生成一个详细的公司画像。\n\n请按照以下 JSON 格式输出，对于无法从文件中获取的字段，请标记为 \"待确认\"。\n\nJSON 格式要求：\n" + str(company_profile_schema) + "\n\n请确保：\n1. 所有字段都有值，缺失的字段标记为 \"待确认\"\n2. 输出的是有效的 JSON 格式\n3. 信息提取要准确，基于 PDF 文件内容\n4. 对于数组类型的字段，如果没有信息，请返回空数组\n\n文件 ID: " + file_id
            
            # 调用 OpenAI API，使用 Structured Outputs
            response = openai.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的外贸获客分析师，擅长从文档中提取公司信息并生成标准化的公司画像。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "generate_company_profile",
                            "description": "生成公司画像",
                            "parameters": company_profile_schema
                        }
                    }
                ],
                tool_choice={"type": "function", "function": {"name": "generate_company_profile"}}
            )
            
            # 解析响应
            if response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                if tool_call.function.name == "generate_company_profile":
                    import json
                    profile = json.loads(tool_call.function.arguments)
                    # 确保所有字段都有值，缺失的标记为 "待确认"
                    profile = self._ensure_all_fields(profile)
                    return profile
            
            # 如果没有工具调用响应，返回错误
            return {"error": "无法生成公司画像"}
            
        except Exception as e:
            raise Exception(f"生成公司画像失败: {str(e)}")
    
    def _ensure_all_fields(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """确保所有字段都有值，缺失的标记为 '待确认'"""
        # 递归遍历 schema，确保所有字段都有值
        def ensure_fields(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
            for key, properties in schema.get("properties", {}).items():
                if key not in data:
                    if properties.get("type") == "array":
                        data[key] = []
                    elif properties.get("type") == "object":
                        data[key] = ensure_fields({}, properties)
                    else:
                        data[key] = "待确认"
                elif properties.get("type") == "object" and isinstance(data[key], dict):
                    data[key] = ensure_fields(data[key], properties)
                elif properties.get("type") == "array" and isinstance(data[key], list):
                    # 确保数组不为 None
                    if data[key] is None:
                        data[key] = []
            return data
        
        return ensure_fields(profile, company_profile_schema)

company_profile_generator = CompanyProfileGenerator()