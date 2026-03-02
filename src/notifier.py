import requests


class Notifier:
    """
    负责将消息推送到各个通知管道
    """

    def __init__(self, config):
        self.config = config.get("notifiers", {})

    def send_discord(self, message):
        webhook_url = self.config.get("discord", {}).get("webhook_url")
        if not webhook_url:
            return
        payload = {"content": message}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print(f"Discord notify failed: {e}")

    def send_feishu(self, message):
        webhook_url = self.config.get("feishu", {}).get("webhook_url")
        if not webhook_url:
            return
        payload = {"msg_type": "text", "content": {"text": message}}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print(f"Feishu notify failed: {e}")

    def send_telegram(self, message):
        bot_token = self.config.get("telegram", {}).get("token")
        chat_id = self.config.get("telegram", {}).get("chat_id")
        if not bot_token or not chat_id:
            return
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Telegram notify failed: {e}")

    def notify_all(self, title, message):
        full_message = f"【{title}】\n{message}"
        # 执行配置中启用的所有通知
        if self.config.get("discord", {}).get("enabled"):
            self.send_discord(full_message)
        if self.config.get("feishu", {}).get("enabled"):
            self.send_feishu(full_message)
        if self.config.get("telegram", {}).get("enabled"):
            self.send_telegram(full_message)

        # 打印到控制台，针对 Windows 处理可能的编码问题
        try:
            print(full_message)
        except UnicodeEncodeError:
            # 如果控制台不支持 emoji，则尝试过滤或忽略
            print(full_message.encode("ascii", "ignore").decode("ascii"))
