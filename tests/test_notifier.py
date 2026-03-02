import unittest
from unittest.mock import patch, MagicMock
from src.notifier import Notifier


class TestNotifier(unittest.TestCase):
    def setUp(self):
        self.config = {
            "notifiers": {
                "wecom": {"enabled": True, "webhook_url": "https://wecom.webhook"},
                "pushplus": {"enabled": True, "token": "pp_token"},
                "serverchan": {"enabled": True, "send_key": "sc_key"},
                "discord": {"enabled": False},
                "feishu": {"enabled": False},
                "telegram": {"enabled": False},
            }
        }
        self.notifier = Notifier(self.config)

    @patch("src.notifier.requests.post")
    def test_send_wecom(self, mock_post):
        self.notifier.send_wecom("test message")
        mock_post.assert_called_once_with(
            "https://wecom.webhook",
            json={"msgtype": "text", "text": {"content": "test message"}},
        )

    @patch("src.notifier.requests.post")
    def test_send_pushplus(self, mock_post):
        self.notifier.send_pushplus("test title", "test message")
        mock_post.assert_called_once_with(
            "http://www.pushplus.plus/send",
            json={
                "token": "pp_token",
                "title": "test title",
                "content": "test message",
                "template": "html",
            },
        )

    @patch("src.notifier.requests.post")
    def test_send_serverchan(self, mock_post):
        self.notifier.send_serverchan("test title", "test message")
        mock_post.assert_called_once_with(
            "https://sctapi.ftqq.com/sc_key.send",
            data={"title": "test title", "desp": "test message"},
        )

    @patch("src.notifier.requests.post")
    def test_notify_all(self, mock_post):
        # notify_all should call wecom, pushplus, and serverchan based on setUp config
        self.notifier.notify_all("Title", "Message")
        # wecom, pushplus, serverchan should have been called
        self.assertEqual(mock_post.call_count, 3)


if __name__ == "__main__":
    unittest.main()
