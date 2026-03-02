import requests
import re


class GoldFetcher:
    """
    负责从公开财经接口获取金价数据
    """

    def __init__(self):
        # 使用新浪财经的简易接口作为示例
        self.sina_api_url = (
            "https://hq.sinajs.cn/list=hf_XAU"  # 国际现货黄金 (美元/盎司)
        )
        self.sina_domestic_api = (
            "https://hq.sinajs.cn/list=gds_AU9999"  # 国内黄金 (元/克)
        )

    def fetch_price(self):
        """
        获取当前金价
        返回格式: {'price': 550.25, 'name': 'Au99.99', 'time': '2024-03-21 14:00:00'}
        """
        try:
            # 获取国内 Au9999 价格
            response = requests.get(
                self.sina_domestic_api,
                headers={"Referer": "http://finance.sina.com.cn"},
            )
            # 新浪接口通常是 GBK 编码
            response.encoding = "gbk"
            content = response.text

            # 调试输出观察到的内容：var hq_str_gds_AU9999="1194.80,0,1194.80,1197.99,1195.00,1144.20,15:08:29,1142.97,1146.00,1482900,637.00,200.00,2026-03-02,99";
            match = re.search(r'="(.+)"', content)
            if match:
                data = match.group(1).split(",")
                # 根据观察到的格式，价格可能在索引 0, 7 或 8
                # 针对 Au9999，通常 data[0] 是最新价
                if len(data) > 12:
                    return {
                        "name": "黄金(Au99.99)",
                        "price": float(data[0]),
                        "time": f"{data[12]} {data[6]}",
                    }
            return None
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None


if __name__ == "__main__":
    fetcher = GoldFetcher()
    print(fetcher.fetch_price())
