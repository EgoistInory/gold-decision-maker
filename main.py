import yaml
import logging
import sys
from src.fetcher import GoldFetcher
from src.strategy import GoldStrategy
from src.notifier import Notifier

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def load_config():
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return {}


def main():
    logger.info("--- 黄金理财决策器启动 ---")

    # 1. 加载配置
    config = load_config()
    if not config:
        logger.error("配置为空或加载失败，请检查 config.yaml")
        return

    # 2. 获取金价
    fetcher = GoldFetcher()
    data = fetcher.fetch_price()

    if not data:
        logger.error("无法获取金价数据，脚本退出。")
        return

    price = data["price"]
    logger.info(f"当前金价 ({data['name']}): {price} 元/克 (更新时间: {data['time']})")

    # 3. 决策逻辑
    strategy = GoldStrategy(config)
    notifier = Notifier(config)

    # 获取所有决策结果
    alerts, suggestions = strategy.get_all_decisions(price)

    # 4. 发送通知
    # 价格预警
    for alert in alerts:
        notifier.notify_all("黄金价格预警", alert)

    # 投资建议 (如果有多个建议，合并发送)
    if suggestions:
        combined_suggestion = "\n".join(suggestions)
        notifier.notify_all("定投决策建议", combined_suggestion)

    logger.info("--- 任务处理完成 ---")


if __name__ == "__main__":
    main()
