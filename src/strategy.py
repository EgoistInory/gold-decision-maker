import datetime


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
        """
        invest_plan = self.config.get("fixed_investment", {})
        if not invest_plan.get("enabled"):
            return None

        # 检查星期几 (0=Mon, 6=Sun)
        target_days = invest_plan.get("day_of_week", [1]) #默认周一
        if isinstance(target_days, int):
            target_days = [target_days]

        today_day = datetime.datetime.now().weekday()

        if today_day in target_days:
            return f"📦 定投建议: 今日是预设的定投日。当前金价 {current_price}。建议执行定投计划。"
        return None

    def check_dip_buy(self, current_price):
        """逢低加仓算法
        当启用且当前价格低于参考价的阈值时，返回加仓建议。
        """
        dip_cfg = self.config.get("dip_buy", {})
        if not dip_cfg.get("enabled"):
            return None

        threshold = dip_cfg.get("threshold", 0.05)  # 默认 5% 下跌
        reference_price = dip_cfg.get("reference_price")

        if reference_price is None or reference_price <= 0:
            return None

        if current_price <= reference_price * (1 - threshold):
            return f"📈 逢低加仓: 当前金价 {current_price} 已低于参考价 {reference_price} 的 {threshold*100:.0f}%，建议适当加仓。"
        return None

    def get_all_decisions(self, current_price):
        """
        运行所有逻辑并按领域聚合结果。
        返回两个对象: (alerts, investment_suggestions)
        """
        alerts = self.check_alerts(current_price)
        investment_suggestions = []

        fixed_msg = self.check_fixed_investment(current_price)
        if fixed_msg:
            investment_suggestions.append(fixed_msg)

        dip_msg = self.check_dip_buy(current_price)
        if dip_msg:
            investment_suggestions.append(dip_msg)

        return alerts, investment_suggestions
