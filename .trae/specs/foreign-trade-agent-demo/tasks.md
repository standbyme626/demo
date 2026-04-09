# 外贸获客智能体 Demo - 实施计划（分解与优先级任务列表）

## [x] 任务 1: 项目初始化
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 建立可运行工程骨架，确保后续模块可并行开发
  - 创建仓库结构：backend/、frontend/、docs/、data/
  - 初始化后端服务
  - 初始化前端单页项目
  - 建立环境变量模板
  - 配置日志、异常处理、基础配置文件
  - 建立 /health 健康检查接口
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8
- **Test Requirements**:
  - `programmatic` TR-1.1: 本地可启动前后端
  - `programmatic` TR-1.2: /health 接口可访问
  - `programmatic` TR-1.3: 前端能访问后端 API
- **Notes**: 项目初始化是后续所有任务的基础，必须首先完成。

## [x] 任务 2: PDF 上传与解析
- **Priority**: P0
- **Depends On**: 任务 1
- **Description**:
  - 实现前端 PDF 上传控件
  - 实现后端文件接收与保存
  - 对接 OpenAI File inputs / Responses API
  - 设计统一文件处理流程
  - 保存原始 PDF 与解析任务状态
- **Acceptance Criteria Addressed**: AC-1
- **Test Requirements**:
  - `programmatic` TR-2.1: 任意 PDF 可上传
  - `programmatic` TR-2.2: 后端能收到文件并进入解析流程
- **Notes**: 技术依据：OpenAI 官方文档说明，Responses API 支持将文件作为 input_file 输入；对于 PDF，模型会提取文本和页面图像一并处理。

## [x] 任务 3: 公司画像生成
- **Priority**: P0
- **Depends On**: 任务 2
- **Description**:
  - 设计 company_profile JSON Schema
  - 编写 PDF→公司画像 prompt
  - 使用 Structured Outputs 约束输出结构
  - 生成标准化公司画像
  - 对缺失字段打 "待确认" 标记
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-3.1: 输出字段完整
  - `programmatic` TR-3.2: 不写死特定公司
  - `programmatic` TR-3.3: 缺失字段会标记，不编造信息
- **Notes**: 技术依据：Structured Outputs 用于保证模型输出符合指定 JSON Schema，比普通 JSON mode 更适合这里的结构化画像。

## [x] 任务 4: 目标客户方向推导
- **Priority**: P0
- **Depends On**: 任务 3
- **Description**:
  - 从公司画像提取目标市场
  - 从公司画像提取优先客群
  - 生成候选客户画像（ICP-lite）
  - 生成不应开发的客户类型
  - 若市场/画像不完整，生成"需补充项"
- **Acceptance Criteria Addressed**: AC-3
- **Test Requirements**:
  - `programmatic` TR-4.1: 能从任意 PDF 提取至少 1 个优先市场
  - `programmatic` TR-4.2: 能给出至少 1 个目标客户方向
  - `programmatic` TR-4.3: 能输出"不适合开发的客户类型"
- **Notes**: 业务依据：样例 PDF 已经展示了这种结构：A/B/C 客户画像、市场优先级、避开客户类型、待确认的认证/MOQ/主力出口国。

## [/] 任务 5: 候选客户搜索（MVP）
- **Priority**: P0
- **Depends On**: 任务 4
- **Description**:
  - 设计搜索输入结构
  - 先实现 2–3 个搜索来源
  - 获取 5–10 家样本客户
  - 规范化客户结果结构
  - 保存搜索来源链接
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-5.1: 输出 5–10 家候选客户
  - `programmatic` TR-5.2: 每家至少有：公司名、国家、官网、来源
  - `programmatic` TR-5.3: 找不到联系方式时标记为"待核实"
- **Notes**: 业务依据：Word 的完整版 Step 1–3 是"市场扫描 → ICP 画像 → 7 维搜索"，并要求候选客户可继续进入评分与触达路径。本轮只实现 MVP 搜索，不做 7 维全量。

## [ ] 任务 6: 客户分级与原因说明
- **Priority**: P0
- **Depends On**: 任务 5
- **Description**:
  - 设计 Demo 版评分模型
  - 设计分级区间
  - 输出分级原因、关键依据、待核实项
  - 支持规则+模型结合
  - 记录分维度得分
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `programmatic` TR-6.1: 每家客户必须有等级
  - `programmatic` TR-6.2: 每家客户必须有原因
  - `programmatic` TR-6.3: 不能只有总分，没有分项依据
  - `programmatic` TR-6.4: 找不到的信息必须体现在不确定性字段里
- **Notes**: 业务依据：Word 明确要求：每轮输出必须包含 ICP 评分+分级；评分必须有分维度依据；没有明确依据不能把客户列为高等级；找不到的信息要写"待核实"。

## [ ] 任务 7: 下一步动作建议
- **Priority**: P0
- **Depends On**: 任务 6
- **Description**:
  - 设计等级→动作规则
  - 输出建议渠道
  - 输出建议时机
  - 输出简短开场话术
  - 输出是否需要人工接管
- **Acceptance Criteria Addressed**: AC-6
- **Test Requirements**:
  - `programmatic` TR-7.1: 每个客户都有动作
  - `programmatic` TR-7.2: 动作与等级有明显映射关系
  - `programmatic` TR-7.3: 不是泛泛而谈的"建议跟进"
- **Notes**: 业务依据：Word 要求输出"最优触达路径：渠道 + 第一句话 + 先联系谁"；同时要求分级开发计划。

## [ ] 任务 8: 飞书多维表落地
- **Priority**: P0
- **Depends On**: 任务 7
- **Description**:
  - 配置飞书应用凭证
  - 建立多维表字段映射
  - 开发写入接口
  - 支持新增记录
  - 回传写入状态
- **Acceptance Criteria Addressed**: AC-7
- **Test Requirements**:
  - `programmatic` TR-8.1: 记录真实写入飞书
  - `programmatic` TR-8.2: 前端显示同步成功/失败
  - `programmatic` TR-8.3: 字段内容与后端结果一致
- **Notes**: 技术依据：飞书多维表新增记录接口要求调用身份具备编辑权限，并通过 POST /bitable/v1/apps/:app_token/tables/:table_id/records 新增记录；多维表每一行就是一条 record，数据通过 fields 表示。

## [ ] 任务 9: 前端单页 Demo
- **Priority**: P0
- **Depends On**: 任务 1, 任务 2, 任务 3, 任务 4, 任务 5, 任务 6, 任务 7, 任务 8
- **Description**:
  - 设计单页信息架构
  - 开发 5 张 Agent 状态卡
  - 开发结果表格
  - 开发单条客户详情抽屉
  - 开发飞书同步状态区
  - 接入后端 API
- **Acceptance Criteria Addressed**: AC-8
- **Test Requirements**:
  - `human-judgment` TR-9.1: 单页可演示完整链路
  - `human-judgment` TR-9.2: 页面不是聊天框
  - `human-judgment` TR-9.3: 能明显看到各 Agent 输入/输出/状态
- **Notes**: 该页面为加分项，但纳入正式交付范围，因为它有助于向非技术角色直观展示"数字员工协同"的概念。

## [ ] 任务 10: 测试、文档、演示准备
- **Priority**: P1
- **Depends On**: 任务 9
- **Description**:
  - 联调前后端
  - 跑 1 个真实 PDF 样例
  - 校验飞书写入
  - 产出 Demo 使用说明
  - 产出 1 页架构图
  - 录制演示或准备现场演示脚本
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8
- **Test Requirements**:
  - `programmatic` TR-10.1: 所有 API 接口正常工作
  - `programmatic` TR-10.2: 完整流程能正常运行
  - `human-judgment` TR-10.3: 文档齐全，演示流畅
- **Notes**: 确保能演示、能交付、能解释。