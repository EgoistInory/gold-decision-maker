# 黄金投资定投理财决策器

该工具实现了金价实时监控、定投策略决策以及多渠道通知推送。

## 主要功能

- **实时金价抓取**：从新浪财经抓取国内 Au99.99 实时价格。
- **智能策略分析**：根据 `config.yaml` 设定的高低价阈值，自动生成买入/卖出预警。
- **多渠道推送**：支持 Discord、飞书、Telegram、企业微信、pushplus、Server酱 通知。
- **自动化运营**：配置了 GitHub Actions，支持按 Cron 周期自动运行，无需本地 24 小时挂机。

## 项目结构

| 文件 | 说明 |
| --- | --- |
| `main.py` | 程序主入口 |
| `src/fetcher.py` | 处理 API 请求与数据解析 |
| `src/strategy.py` | 包含价格预警和定投买入逻辑 |
| `src/notifier.py` | 集成多个推送通道，密钥优先读取环境变量 |
| `config.yaml` | 用户配置中心（阈值、定投、通知开关） |
| `.github/workflows/schedule.yml` | GitHub Actions 定时工作流 |

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 本地运行
python main.py
```

## 通知配置

所有推送 Token / Webhook 均优先读取**环境变量**，其次回退到 `config.yaml`。

| 通道 | 环境变量 | config.yaml 字段 |
| --- | --- | --- |
| Discord | `DISCORD_WEBHOOK` | `notifiers.discord.webhook_url` |
| 飞书 | `FEISHU_WEBHOOK` | `notifiers.feishu.webhook_url` |
| Telegram | `TELEGRAM_TOKEN` / `TELEGRAM_CHAT_ID` | `notifiers.telegram.token` / `chat_id` |
| 企业微信 | `WECHAT_WEBHOOK` | `notifiers.wecom.webhook_url` |
| pushplus | `PUSHPLUS_TOKEN` | `notifiers.pushplus.token` |
| Server酱 | `SERVERCHAN_SEND_KEY` | `notifiers.serverchan.send_key` |

> **部署到 GitHub 时**，请将密钥添加到 **Repo Settings → Secrets**，工作流会自动注入。

## 后续建议

- **定投逻辑**：目前定投基于 `config.yaml` 简单触发，可在 `src/strategy.py` 中添加更复杂的"逢低加仓"算法。
- **数据源扩展**：可在 `src/fetcher.py` 中接入更多数据源以提高可靠性。