# 外贸获客智能体 Demo 项目

这是一个外贸获客智能体的 Demo 项目，基于 PDF 驱动的智能获客系统，能够自动完成公司画像识别、候选客户获取、客户分级、动作建议、飞书落地及流程可视化展示。

## 项目结构

```
.
├── backend/          # FastAPI 后端服务
├── frontend/         # Vite + React 前端项目
├── demo/             # Demo 文档和资源
│   ├── DEMO_GUIDE.md          # Demo 使用说明
│   ├── ARCHITECTURE.md        # 架构设计文档
│   ├── ARCHITECTURE_DIAGRAM.md # Mermaid 架构图
│   ├── DEMO_SCRIPT.md         # 演示脚本
│   └── sample_company_profile.md # 示例公司资料
└── README.md          # 项目说明
```

## 功能特性

- ✅ PDF 上传与解析
- ✅ 公司画像自动生成
- ✅ 目标客户方向推导
- ✅ 候选客户智能搜索
- ✅ 客户 A/B/C/D 分级
- ✅ 下一步动作建议生成
- ✅ 飞书多维表数据同步
- ✅ 多 Agent 可视化界面
- ✅ 完整的 API 接口

## 技术栈

### 后端
- **框架**: FastAPI
- **语言**: Python 3.8+
- **AI 服务**: OpenAI API (Responses API)
- **数据集成**: Feishu Bitable API
- **其他**: Uvicorn, Pydantic, python-dotenv

### 前端
- **框架**: React 19
- **构建工具**: Vite
- **UI 组件**: Ant Design
- **语言**: JavaScript

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- OpenAI API Key
- 飞书应用凭证（可选）

### 后端服务

1. 进入 backend 目录
```bash
cd /workspace/backend
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 OpenAI API Key 和飞书配置
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行服务
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端项目

1. 进入 frontend 目录
```bash
cd /workspace/frontend
```

2. 安装依赖
```bash
npm install
```

3. 运行开发服务器
```bash
npm run dev
```

4. 在浏览器中访问：http://localhost:5173

## Demo 文档

- **[Demo 使用说明](./demo/DEMO_GUIDE.md)**: 详细的使用指南和 API 文档
- **[架构设计文档](./demo/ARCHITECTURE.md)**: 系统架构和组件说明
- **[Mermaid 架构图](./demo/ARCHITECTURE_DIAGRAM.md)**: 可视化架构图
- **[演示脚本](./demo/DEMO_SCRIPT.md)**: 现场演示脚本和话术
- **[示例公司资料](./demo/sample_company_profile.md)**: 测试用的公司资料

## API 接口

### 健康检查
```
GET /health
```

### 上传 PDF
```
POST /upload/pdf
Content-Type: multipart/form-data
```

### 生成公司画像
```
POST /generate-profile/{file_id}
```

### 生成客户策略
```
POST /generate-strategy
Content-Type: application/json
```

### 搜索客户
```
POST /search-customers
Content-Type: application/json
```

### 客户分级
```
POST /grade-customers
Content-Type: application/json
```

### 生成动作建议
```
POST /generate-action-suggestions
Content-Type: application/json
```

### 飞书相关接口
```
GET /feishu/test-connection
GET /feishu/fields
GET /feishu/mapping
POST /feishu/mapping
POST /feishu/add-record
POST /feishu/add-records-batch
```

## 项目核心价值

1. **通用性** - 不依赖特定公司，任意 PDF 都能驱动
2. **可解释性** - 每个决策都有依据，不是黑盒
3. **可落地** - 直接对接飞书，能立即用起来
4. **可视化** - 清晰展示 Agent 协作过程

## 未来扩展

- 7 维全量客户挖掘
- 海关数据深挖
- 竞品客户渗透
- 多市场并发切换
- 支持更多 CRM 系统集成

## 许可证

MIT License
