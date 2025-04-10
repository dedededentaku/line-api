import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

LINE_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
USER_ID = os.environ.get("LINE_USER_ID")
INPUT_FILE = "data/filtered_programs.json"

def send_line_message(text):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    payload = {
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.ok

def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        programs = json.load(f)

    if programs:
        msg = "📺 今週はイッテQあります！やったね！\n"
        for p in programs:
            msg += f"\n▶ {p['title']}\n🕒 {p['start_time']}\n{p['detail']}\n"
    else:
        msg = "📡 今週はイッテQありません。しょぼぼぼ･･･"

    success = send_line_message(msg)
    print("通知送信結果:", "成功" if success else "失敗")

if __name__ == "__main__":
    main()
