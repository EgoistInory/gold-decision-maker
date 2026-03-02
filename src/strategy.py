class GoldStrategy:
    """
    负责基于配置和金价进行策略决策
    """

    def __init__(self, config):
        self.config = config

    def check_alerts(self, current_price):
        """
        检查金价是否触发预警
        """
        alerts = []
        low_threshold = self.config.get("thresholds", {}).get("low")
        high_threshold = self.config.get("thresholds", {}).get("high")

        if low_threshold and current_price <= low_threshold:
            alerts.append(
                f"🔴 低价预警: 当前金价 {current_price} 已达到或低于设定值 {low_threshold}。建议买入。"
            )

        if high_threshold and current_price >= high_threshold:
            alerts.append(
                f"🟢 高价预警: 当前金价 {current_price} 已达到或高于设定值 {high_threshold}。建议止盈。"
            )

        return alerts

    def check_fixed_investment(self, current_price):
        """
        检查今日是否符合定投条件
        示例逻辑：每周固定的定投日进行买入提示
        """
        # 这里可以扩展更复杂的定投逻辑，目前仅返回简单的买入建议占位
        invest_plan = self.config.get("fixed_investment", {})
        if not invest_plan.get("enabled"):
            return None

        # 简单示范：如果启用定投，且符合某个逻辑（此处暂简略）
        return f"📦 定投建议: 当前金价 {current_price}。根据计划，今日建议定投买入。"

    def check_dip_buy(self, current_price):
        """逢低加仓算法
        当启用且当前价格低于参考价的阈值时，返回加仓建议。
        配置示例在 config.yaml 中的 `dip_buy` 节点。
        """
        dip_cfg = self.config.get("dip_buy", {})
        if not dip_cfg.get("enabled"):
            return None
        threshold = dip_cfg.get("threshold", 0.05)  # 默认 5% 下跌
        reference_price = dip_cfg.get("reference_price")
        if reference_price is None or reference_price <= 0:
            return None
        if current_price <= reference_price * (1 - threshold):
            return f"📈 逢低加仓: 当前金价 {current_price} 已低于参考价 {reference_price} 的 {threshold*100:.0f}%，建议加仓。"
        return None
