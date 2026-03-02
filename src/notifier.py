import os

import requests


class Notifier:
    """
    负责将消息推送到各个通知管道。
    密钥/Token 优先读取环境变量，其次回退到 config.yaml 中的配置。
    """

    def __init__(self, config):
        self.config = config.get("notifiers", {})

    def _get(self, section, key, env_var=None):
        """优先读取环境变量，否则从 config 中取值。"""
        if env_var:
            val = os.environ.get(env_var)
            if val:
                return val
        return self.config.get(section, {}).get(key)

    def send_discord(self, message):
        webhook_url = self._get("discord", "webhook_url", "DISCORD_WEBHOOK")
        if not webhook_url:
            return
        payload = {"content": message}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print(f"Discord notify failed: {e}")

    def send_feishu(self, message):
        webhook_url = self._get("feishu", "webhook_url", "FEISHU_WEBHOOK")
        if not webhook_url:
            return
        payload = {"msg_type": "text", "content": {"text": message}}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print(f"Feishu notify failed: {e}")

    def send_telegram(self, message):
        bot_token = self._get("telegram", "token", "TELEGRAM_TOKEN")
        chat_id = self._get("telegram", "chat_id", "TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id:
            return
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Telegram notify failed: {e}")

    def send_wecom(self, message):
        webhook_url = self._get("wecom", "webhook_url", "WECHAT_WEBHOOK")
        if not webhook_url:
            return
        payload = {"msgtype": "text", "text": {"content": message}}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print(f"WeCom notify failed: {e}")

    def send_pushplus(self, title, message):
        token = self._get("pushplus", "token", "PUSHPLUS_TOKEN")
        if not token:
            return
        payload = {
            "token": token,
            "title": title,
            "content": message,
            "template": "html",
        }
        try:
            requests.post("http://www.pushplus.plus/send", json=payload)
        except Exception as e:
            print(f"Pushplus notify failed: {e}")

    def send_serverchan(self, title, message):
        send_key = self._get("serverchan", "send_key", "SERVERCHAN_SEND_KEY")
        if not send_key:
            return
        url = f"https://sctapi.ftqq.com/{send_key}.send"
        payload = {"title": title, "desp": message}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"ServerChan notify failed: {e}")

    def notify_all(self, title, message):
        full_message = f"【{title}】\n{message}"
        # 执行配置中启用的所有通知
        if self.config.get("discord", {}).get("enabled"):
            self.send_discord(full_message)
        if self.config.get("feishu", {}).get("enabled"):
            self.send_feishu(full_message)
        if self.config.get("telegram", {}).get("enabled"):
            self.send_telegram(full_message)
        if self.config.get("wecom", {}).get("enabled"):
            self.send_wecom(full_message)
        if self.config.get("pushplus", {}).get("enabled"):
            self.send_pushplus(title, message)
        if self.config.get("serverchan", {}).get("enabled"):
            self.send_serverchan(title, message)

        # 打印到控制台，针对 Windows 处理可能的编码问题
        try:
            print(full_message)
        except UnicodeEncodeError:
            # 如果控制台不支持 emoji，则尝试过滤或忽略
            print(full_message.encode("ascii", "ignore").decode("ascii"))
