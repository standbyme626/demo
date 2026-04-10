# Google Custom Search API 获取指南

## 步骤 1: 创建 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 点击左上角的项目选择器
3. 点击「新建项目」按钮
4. 输入项目名称（例如 "Foreign Trade Customer Search"）
5. 点击「创建」按钮

## 步骤 2: 启用 Custom Search API

1. 在项目仪表板中，点击「API 和服务」>「库」
2. 在搜索框中输入 "Custom Search API"
3. 点击「Google Custom Search API」
4. 点击「启用」按钮

## 步骤 3: 创建 API 密钥

1. 点击「API 和服务」>「凭据」
2. 点击「创建凭据」>「API 密钥」
3. 复制生成的 API 密钥（稍后会用到）
4. （可选）点击「限制密钥」来设置使用限制

## 步骤 4: 创建自定义搜索引擎

1. 访问 [Google Custom Search Engine](https://cse.google.com/cse/all)
2. 点击「添加」按钮
3. 输入搜索引擎名称（例如 "Trade Customer Search"）
4. 在「网站」字段中，可以输入一些相关的 B2B 网站，例如：
   - `*.alibaba.com`
   - `*.made-in-china.com`
   - `*.globalsources.com`
   - `*.dhgate.com`
5. 点击「创建」按钮
6. 记录下生成的搜索引擎 ID（cx 参数）

## 步骤 5: 配置搜索设置

1. 在自定义搜索引擎管理页面，点击「修改搜索引擎」
2. 在「基本」设置中，确保启用「搜索整个网络」选项
3. 调整其他设置以满足您的需求
4. 点击「更新」按钮

## 步骤 6: 集成到代码中

### 后端集成

修改 `/workspace/backend/app/api/customer_search.py` 文件，替换模拟搜索逻辑：

```python
import requests
from fastapi import APIRouter, Query
from typing import List, Dict, Any

router = APIRouter()

# 配置 Google Custom Search API
GOOGLE_API_KEY = "您的API密钥"
SEARCH_ENGINE_ID = "您的搜索引擎ID"

def search_google_custom(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """使用 Google Custom Search API 搜索客户信息"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results,
        "gl": "us"  # 搜索地区设置
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        
        # 处理搜索结果
        search_results = []
        if "items" in results:
            for item in results["items"]:
                search_results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "Google Custom Search"
                })
        
        return search_results
    except Exception as e:
        print(f"搜索错误: {e}")
        return []

@router.get("/search", response_model=List[Dict[str, Any]])
async def search_customers(
    query: str = Query(..., description="搜索关键词"),
    source: str = Query("all", description="搜索来源: all, google, bing, linkedin")
):
    """搜索客户信息"""
    results = []
    
    if source == "all" or source == "google":
        google_results = search_google_custom(query)
        results.extend(google_results)
    
    # 可以添加其他搜索源
    
    return results
```

### 环境变量配置

建议将 API 密钥存储在环境变量中，而不是硬编码在代码中：

1. 在 `/workspace/backend/.env` 文件中添加：
   ```
   GOOGLE_API_KEY=您的API密钥
   SEARCH_ENGINE_ID=您的搜索引擎ID
   ```

2. 修改代码以读取环境变量：
   ```python
   import os
   from dotenv import load_dotenv
   
   # 加载环境变量
   load_dotenv()
   
   # 配置 Google Custom Search API
   GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
   SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
   ```

## 步骤 7: 测试 API

1. 启动后端服务
2. 访问 `http://localhost:8000/api/customer/search?query=electronics%20supplier`
3. 检查返回的搜索结果

## 注意事项

1. **免费额度**：Google Custom Search API 提供每天 100 次免费搜索请求
2. **超出限制**：超出免费额度后，每 1000 次查询费用约为 $5
3. **搜索质量**：可以通过调整自定义搜索引擎的设置来提高搜索质量
4. **API 密钥安全**：不要在代码中硬编码 API 密钥，使用环境变量或密钥管理服务

## 故障排除

- 如果遇到 API 错误，检查 API 密钥是否正确
- 确保已启用 Custom Search API
- 检查搜索引擎 ID 是否正确
- 查看 Google Cloud Console 中的 API 使用情况

## 替代方案

如果 Google Custom Search API 不满足需求，可以考虑：

1. **Bing Web Search API**：提供每月 1000 次免费查询
2. **SerpAPI**：统一的搜索 API 接口，支持多个搜索引擎
3. **直接网页爬虫**：自行开发爬虫抓取 B2B 网站数据（注意遵守网站 robots.txt）

希望这份指南能帮助您成功集成 Google Custom Search API 到客户搜索功能中！