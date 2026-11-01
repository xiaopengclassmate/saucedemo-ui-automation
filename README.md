# Saucedemo Web UI 自动化测试框架

基于 **Python + Playwright + Pytest + Page Object + Allure + GitHub Actions** 的电商网站端到端自动化测试项目。

被测站点：[Sauce Demo](https://www.saucedemo.com/)（Sauce Labs 官方公开练习站，无需注册、数据稳定）。

## 项目亮点

- **Page Object 分层**：页面元素与操作封装在 `pages/`，用例只表达业务语义，元素改版时只需改一处。
- **数据驱动**：登录正/负向用例全部来自 `data/login_cases.yaml`，新增用例不改代码。
- **稳定的等待策略**：不写 `sleep`，统一使用 Playwright 自动等待与 `expect` 断言。
- **失败可观测**：用例失败自动截图、记录页面 URL 与浏览器控制台日志，并附加到 Allure 报告。
- **工程化接入**：pytest marker 分层（smoke/regression/negative）、并发执行、Allure 报告、GitHub Actions 每日定时回归。
- **覆盖完整业务闭环**：登录 → 商品列表 → 排序 → 购物车 → 结算 → 下单成功。

## 测试范围

| 模块 | 用例数 | 覆盖内容 |
|---|---:|---|
| 登录 | 5 | 正常登录、锁定用户、错误密码、用户名/密码必填 |
| 商品列表 | 5 | 商品数量、价格升/降序、购物车角标增减、退出登录 |
| 下单 | 2 | 完整下单流程、邮编必填校验 |
| **合计** | **12** | 冒烟 + 回归 + 异常场景 |

## 目录结构

```text
saucedemo-ui-automation/
├── config/
│   └── settings.py          # 环境变量与超时配置
├── data/
│   └── login_cases.yaml     # 数据驱动用例
├── pages/                   # Page Object
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   └── test_checkout.py
├── utils/
│   └── data_loader.py
├── conftest.py              # fixture、失败截图、Allure 附加
├── pytest.ini
├── requirements.txt
└── .github/workflows/ui-tests.yml
```

## 快速开始

```bash
# 1. 安装依赖
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m playwright install chromium

# 2. 准备配置（可选）
cp .env.example .env

# 3. 运行全部用例
pytest
```

## 常用命令

```bash
pytest                       # 全部用例
pytest -m smoke              # 只跑冒烟用例
pytest -m regression         # 只跑回归用例
pytest -m negative           # 只跑异常场景
pytest --headed              # 有界面模式，方便调试
pytest -n auto               # 多进程并发
pytest tests/test_login.py   # 只跑登录模块
pytest -k "checkout"         # 按名称过滤
```

## 测试报告

项目同时输出两份报告：

```bash
# Pytest HTML：reports/report.html，直接用浏览器打开
# Allure：生成并查看
allure serve allure-results
```

Allure CLI 安装方式（任选其一）：

```bash
npm install -g allure-commandline
# 或 Windows: scoop install allure
```

CI 中会自动生成 Allure 报告并发布到 GitHub Pages。

## CI 流水线

`.github/workflows/ui-tests.yml` 在以下场景触发：

- push 到 `main` / `master`
- Pull Request
- 手动触发（workflow_dispatch）
- 每天 01:00 UTC 定时回归

流水线步骤：安装依赖 → 安装 Chromium → 执行测试 → 上传 HTML/Allure 产物 → 生成并发布 Allure 报告。

## 设计说明（面试可讲）

1. **为什么选 Playwright？**
   自动等待、trace、多浏览器、网络拦截、速度快；相比 Selenium 少了显式等待和 driver 管理。
2. **Page Object 解决什么问题？**
   页面定位器与业务流程解耦；元素变更只改页面类；用例可读性接近自然语言。
3. **如何避免 flaky？**
   不使用固定 sleep；用 `expect` 轮询断言；对动态渲染页面等待关键元素/数量；失败自动截图和日志便于定位。
4. **测试数据怎么管理？**
   正负向登录数据放 YAML，由 `pytest.mark.parametrize` 注入；环境和账号配置走 `.env`，不硬编码。
5. **CI 怎么落地？**
   定时回归 + PR 门禁；报告作为 artifact 保留；主分支自动发布 Allure 到 GitHub Pages。

## 简历表述参考

> 独立设计并实现基于 Playwright + Pytest 的 Web UI 自动化框架，覆盖登录、商品、购物车、下单 4 个业务模块共 12 条用例；采用 Page Object 与 YAML 数据驱动，接入 Allure 报告、失败自动截图、并发执行与 GitHub Actions 每日定时回归，全量回归约 22 秒。

## 说明

Sauce Demo 是公开练习站点，项目仅用于学习与演示；测试账号为该站点公开提供的演示账号。
