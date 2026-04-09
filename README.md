# 外贸获客智能体 Demo 项目

这是一个外贸获客智能体的 Demo 项目，包含后端和前端部分。

## 项目结构

```
.
├── backend/          # FastAPI 后端服务
├── frontend/         # Vite + React 前端项目
├── docs/             # 项目文档
└── data/             # 数据存储
```

## 快速开始

### 后端服务

1. 进入 backend 目录
2. 安装依赖：`pip install -r requirements.txt`
3. 运行服务：`uvicorn app:app --reload`

### 前端项目

1. 进入 frontend 目录
2. 安装依赖：`npm install`
3. 运行开发服务器：`npm run dev`

## 功能特性

- 健康检查接口：`/health`
- 完整的后端配置和异常处理
- 前端环境变量配置

## 技术栈

- 后端：FastAPI, Python
- 前端：React, Vite
