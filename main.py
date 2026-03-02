import yaml
from src.fetcher import GoldFetcher
from src.strategy import GoldStrategy
from src.notifier import Notifier


def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    print("--- 黄金理财决策器启动 ---")

    # 1. 加载配置
    config = load_config()

    # 2. 获取金价
    fetcher = GoldFetcher()
    data = fetcher.fetch_price()

    if not data:
        print("无法获取金价数据，脚本退出。")
        return

    price = data["price"]
    print(f"当前金价 ({data['name']}): {price} 元/克 (更新时间: {data['time']})")

    # 3. 决策逻辑
    strategy = GoldStrategy(config)
    notifier = Notifier(config)

    # 检查预警
    alerts = strategy.check_alerts(price)
    for alert in alerts:
        notifier.notify_all("黄金价格预警", alert)

    # 检查定投 (此处逻辑可根据 Action 触发频率精细化，暂全量运行)
    invest_msg = strategy.check_fixed_investment(price)
    if invest_msg:
        notifier.notify_all("定投决策建议", invest_msg)

    print("--- 任务处理完成 ---")


if __name__ == "__main__":
    main()
