# ChatGPT Project Brief

> 本文件只保存长期稳定、仓库级的信息。当前任务、临时分支、SHA、测试状态和执行进度应保存在当前 Pull Request 正文中。

## 1. Project

- 项目名称：AmazonComment Spider in Scrapy
- GitHub 仓库：`ychenracing/amazon_comment`
- 默认分支：`master`
- 系统定位：使用 Scrapy 抓取 Amazon.com 商品及评论的简单 Python 爬虫。
- 项目最终目标：从商品搜索和详情/评论页面提取商品与评论字段；更长期目标未在仓库文档中明确。

## 2. Purpose and Non-Goals

项目从固定的 Amazon.com 搜索入口开始，发现商品详情和评论页面，并产生商品、评分、标题、用户、日期、评论及支持人数等 Item。

长期非目标未在仓库文档中明确。仓库不包含 Web 服务、用户界面、发布流程或通用爬虫平台的说明，不应自行假定这些职责。

## 3. Architecture and Module Boundaries

- `amazon_comment/spiders/comment_spider.py`：定义 `amazon_comment` Spider、请求链和页面字段提取。
- `amazon_comment/items.py`：定义商品与评论的 Scrapy Item schema。
- `amazon_comment/settings.py`：定义 Spider 模块和 Scrapy 运行设置；`ROBOTSTXT_OBEY` 为启用状态。
- `amazon_comment/pipelines.py`：提供可选 MySQL 持久化管道；仓库设置中该管道默认未启用。
- `scrapy.cfg`：把默认 Scrapy settings 指向 `amazon_comment.settings`。

数据流：搜索页 → 商品详情页 → 评论页 → `AmazonProductItem` / `AmazonCommentItem` → 可选 Item Pipeline。

Spider 是请求与解析流程 Owner；Item 类是字段 schema Owner；Scrapy settings 是运行配置 Owner。不得在治理文档中建立第二份可执行配置或数据 schema。

## 4. Non-Negotiable Constraints

- 只记录能够从仓库核验的行为；Amazon 页面结构和可用性属于外部依赖。
- 抓取逻辑应继续遵守仓库中已启用的 `ROBOTSTXT_OBEY = True`，除非项目所有者明确批准变更。
- Item 字段由 `amazon_comment/items.py` 定义；持久化逻辑不得悄然改变其含义。
- 数据库配置和凭据不得复制到治理文档、PR 模板或日志中。
- 当前代码面向旧版 Python/Scrapy 语法；未在仓库中定义现代化或兼容性目标，不得擅自假定。

## 5. Authoritative Sources

- 项目定位：`README.md`
- 工程约定：`AGENTS.md`
- Scrapy 入口：`scrapy.cfg`
- 运行设置：`amazon_comment/settings.py`
- Item schema：`amazon_comment/items.py`
- 请求与解析流程：`amazon_comment/spiders/comment_spider.py`
- 可选持久化：`amazon_comment/pipelines.py`
- 依赖、数据库 schema、版本和发布权威来源：未在仓库文档中明确

## 6. Standard Commands

- 安装：未在仓库中定义。
- 构建：不适用；仓库未定义构建流程。
- 单元测试、集成测试、lint、类型检查和格式检查：未在仓库中定义。
- 本地运行：`scrapy.cfg` 与 Spider 名称支持 `scrapy crawl amazon_comment`，但所需 Python、Scrapy、MySQL Connector 版本及环境准备未在仓库中定义。
- 关键验收命令：未在仓库中定义。

## 7. Important Paths

- `amazon_comment/spiders/comment_spider.py`：Spider 和页面解析。
- `amazon_comment/items.py`：商品与评论字段定义。
- `amazon_comment/settings.py`：Scrapy 设置。
- `amazon_comment/pipelines.py`：可选 MySQL 持久化。
- `amazon_comment/middlewares.py`：Scrapy 中间件扩展点。
- `scrapy.cfg`：Scrapy 项目入口。
- `README.md`：项目简介。
- `AGENTS.md`：渐进式验证约定。

## 8. CI and Acceptance Entry Points

- 仓库没有 `.github/workflows/`，未定义 GitHub Actions 构建、测试、lint 或发布门。
- 本地验证应遵循 `AGENTS.md` 的影响范围驱动原则。
- Definition of Done 的项目特有部分未在仓库中定义；变更至少应保持配置可解析、Spider 可加载，并按影响范围验证解析与 Item 行为。

## 9. Prohibited Actions

- 不得把外部 Amazon 页面结构或运行可用性写成仓库内已保证事实。
- 不得在治理文件中记录数据库凭据或其他秘密。
- 不得擅自改写 Git 历史或 force push。
- 不得丢弃未知或未提交工作，也不得覆盖无关改动。
- 不得把计划执行写成已验证完成。
- 不得根据旧聊天猜测当前分支、SHA、PR 或 CI 状态。

## 10. Context Loading Protocol

1. 新开发任务可以直接使用自然语言提出，不要求预先填写固定 Prompt。
2. 开始任务时先读取本文件。
3. 搜索与任务相关的开放 PR、分支和 Issue。
4. 如果存在匹配工作，从现有现场原地继续。
5. 当前动态任务状态默认维护在 Pull Request 正文。
6. 不强制普通单 PR 任务创建 Issue。
7. 优先读取目标代码、直接调用者、相关测试和直接相关配置。
8. 只有证据不足、状态冲突或影响范围扩大时才扩大读取。
9. 不默认加载完整仓库、完整聊天、完整日志或全部 GitHub Actions 历史。
10. 长对话交接使用 `conversation-continuity-guard`，但 GitHub 当前现场仍是状态权威来源。

## 11. References

- `README.md`
- `AGENTS.md`
- `scrapy.cfg`
- `amazon_comment/settings.py`
- `amazon_comment/items.py`
- `amazon_comment/spiders/comment_spider.py`
- `amazon_comment/pipelines.py`
