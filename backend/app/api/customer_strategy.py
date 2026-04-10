from typing import Dict, Any, List, Optional
import openai
from app.config.config import settings

# 初始化 OpenAI 客户端
openai.api_key = settings.OPENAI_API_KEY

# 客户策略 JSON Schema
customer_strategy_schema = {
    "type": "object",
    "properties": {
        "recommended_markets": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "推荐的目标市场"
        },
        "recommended_segments": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "推荐的优先客群"
        },
        "avoid_segments": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "不应开发的客户类型"
        },
        "icp_lite": {
            "type": "object",
            "properties": {
                "company_size": {
                    "type": "string",
                    "description": "公司规模"
                },
                "industry": {
                    "type": "string",
                    "description": "所属行业"
                },
                "location": {
                    "type": "string",
                    "description": "地理位置"
                },
                "annual_spending": {
                    "type": "string",
                    "description": "年度采购额"
                },
                "key_decision_makers": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "关键决策者"
                },
                "pain_points": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "痛点"
                }
            },
            "description": "候选客户画像（ICP-lite）"
        },
        "missing_fields": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "需补充项"
        }
    },
    "required": ["recommended_markets", "recommended_segments", "avoid_segments", "icp_lite", "missing_fields"]
}

class CustomerStrategyGenerator:
    def __init__(self):
        pass
    
    def generate_customer_strategy(self, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """基于公司画像生成客户策略"""
        try:
            # 构建 prompt
            prompt = f'你是一个专业的外贸获客策略师，请基于以下公司画像，生成目标客户方向推导结果。\n\n公司画像：\n{str(company_profile)}\n\n请按照以下 JSON 格式输出，确保包含以下内容：\n1. 从公司画像提取目标市场\n2. 从公司画像提取优先客群\n3. 生成候选客户画像（ICP-lite）\n4. 生成不应开发的客户类型\n5. 若市场/画像不完整，生成"需补充项"\n\nJSON 格式要求：\n{str(customer_strategy_schema)}\n\n请确保：\n1. 所有字段都有值，缺失的字段标记为 "待确认"\n2. 输出的是有效的 JSON 格式\n3. 信息提取要准确，基于公司画像内容\n4. 对于数组类型的字段，如果没有信息，请返回空数组\n'
            
            # 调用 OpenAI API，使用 Structured Outputs
            response = openai.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的外贸获客策略师，擅长基于公司画像推导目标客户方向。"
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
                            "name": "generate_customer_strategy",
                            "description": "生成客户策略",
                            "parameters": customer_strategy_schema
                        }
                    }
                ],
                tool_choice={"type": "function", "function": {"name": "generate_customer_strategy"}}
            )
            
            # 解析响应
            if response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                if tool_call.function.name == "generate_customer_strategy":
                    import json
                    strategy = json.loads(tool_call.function.arguments)
                    # 确保所有字段都有值，缺失的标记为 "待确认"
                    strategy = self._ensure_all_fields(strategy)
                    return strategy
            
            # 如果没有工具调用响应，返回错误
            return {"error": "无法生成客户策略"}
            
        except Exception as e:
            raise Exception(f"生成客户策略失败: {str(e)}")
    
    def _ensure_all_fields(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
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
        
        return ensure_fields(strategy, customer_strategy_schema)

customer_strategy_generator = CustomerStrategyGenerator()