import unittest
from src.strategy import GoldStrategy


class TestGoldStrategy(unittest.TestCase):
    def setUp(self):
        self.config = {
            "thresholds": {"low": 500, "high": 600},
            "fixed_investment": {
                "enabled": True,
                "day_of_week": [0, 1, 2, 3, 4],
            },  # Mon, Tue, Wed
            "dip_buy": {"enabled": True, "threshold": 0.1, "reference_price": 550},
        }
        self.strategy = GoldStrategy(self.config)

    def test_check_alerts(self):
        # 触发高价
        alerts = self.strategy.check_alerts(610)
        self.assertTrue(any("高价预警" in a for a in alerts))

        # 触发低价
        alerts = self.strategy.check_alerts(490)
        self.assertTrue(any("低价预警" in a for a in alerts))

        # 无触发
        alerts = self.strategy.check_alerts(550)
        self.assertEqual(len(alerts), 0)

    def test_check_dip_buy(self):
        # 跌幅超过 10% (550 * 0.9 = 495)
        msg = self.strategy.check_dip_buy(490)
        self.assertIsNotNone(msg)
        self.assertIn("建议适当加仓", msg)

        # 跌幅不足
        msg = self.strategy.check_dip_buy(500)
        self.assertNone(msg)

    def test_get_all_decisions(self):
        # 模拟各种触发
        alerts, suggestions = self.strategy.get_all_decisions(490)
        # 490 触发了低价预警 (thresholds.low=500)
        self.assertEqual(len(alerts), 1)
        # 490 触发了逢低加仓 (reference=550, threshold=0.1)
        self.assertTrue(any("加仓" in s for s in suggestions))


if __name__ == "__main__":
    unittest.main()
