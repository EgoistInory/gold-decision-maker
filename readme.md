黄金投资定投理财决策器 - 交付说明
该工具实现了金价实时监控、定投策略决策以及多渠道通知推送。

主要功能
实时金价抓取：从新浪财经抓取国内 Au99.99 实时价格。
智能策略分析：根据 
config.yaml
 设定的高低价阈值，自动生成买入/卖出预警。
多渠道推送：支持 Discord, Feishu (飞书), Telegram Webhook 通知。
自动化运营：配置了 GitHub Actions，支持按设定的 Cron 周期自动运行，无需本地 24 小时挂机。
项目结构
fetcher.py
: 处理 API 请求与数据解析。
strategy.py
: 包含价格预警和定投买入逻辑。
notifier.py
: 集成多个 Webhook 通道，支持 Windows 编码兼容处理。
main.py
: 程序主入口。
config.yaml
: 用户配置中心。
schedule.yml
: GitHub Actions 工作流。
验证结果
本地运行测试：成功获取金价（当前约 1197.0 元/克）并输出决策建议。
编码兼容性：解决了 Windows 控制台下输出 emoji 导致的 UnicodeEncodeError。
解析修正：针对新浪财经最新的 JS 响应格式进行了匹配修正。
后续建议
Secret 管理：在部署到 GitHub 时，请务必将 Webhook URL 放入 GitHub Repo Secrets，并在 
schedule.yml
 中通过环境变量注入，不要直接写在代码中。
定投逻辑：目前的定投逻辑基于 
config.yaml
 简单触发，可根据实际需求在 
strategy.py
 中添加更复杂的“逢低加仓”算法。