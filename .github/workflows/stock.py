import requests
from bs4 import BeautifulSoup
import os

# =========================
# 設定
# =========================

# チェックしたい商品のページURL
PRODUCT_URL = "ここに商品のURLを入れる"

# Discord Webhook URL
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# 在庫ありと判断する言葉
STOCK_WORDS = [
    "在庫あり",
    "カートに入れる",
    "購入する",
    "販売中"
]


# =========================
# 在庫チェック
# =========================

def check_stock():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 "
            "like Mac OS X) AppleWebKit/605.1.15 "
            "Version/17.0 Mobile/15E148 Safari/604.1"
        )
    }

    response = requests.get(
        PRODUCT_URL,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    for word in STOCK_WORDS:
        if word in text:
            return True, word

    return False, None


# =========================
# Discord通知
# =========================

def send_notification(word):
    message = (
        "🔥 ドラゴンボール商品が在庫あり！\n\n"
        f"判定：{word}\n"
        f"商品ページ：{PRODUCT_URL}"
    )

    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message},
        timeout=20
    )


# =========================
# 実行
# =========================

if __name__ == "__main__":
    try:
        in_stock, word = check_stock()

        if in_stock:
            print(f"在庫あり！ → {word}")
            send_notification(word)
        else:
            print("まだ在庫なし")

    except Exception as e:
        print(f"エラー：{e}")
