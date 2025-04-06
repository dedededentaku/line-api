import json
from datetime import datetime, timedelta

INPUT_FILE = "data/program_data.json"
OUTPUT_FILE = "data/filtered_programs.json"

# 次の日曜日の日付を計算（今日が日曜なら来週）
today = datetime.now().date()
weekday = today.weekday()
days_ahead = 7 if weekday == 6 else (6 - weekday)
target_date = today + timedelta(days=days_ahead)
print(f"🔍 Target date: {target_date}")

# 抽出条件の時間
target_start = datetime.combine(target_date, datetime.min.time()).replace(hour=18)
target_end = datetime.combine(target_date, datetime.min.time()).replace(hour=22)

# JSONファイル読み込み
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    programs = json.load(f)

filtered = []
for p in programs:
    title = p["title"]
    program_start = datetime.strptime(p["start_time"], "%Y-%m-%d %H:%M")
    program_end = datetime.strptime(p["end_time"], "%Y-%m-%d %H:%M")

    # 条件：タイトルに「イッテQ」、18時以降、22時まで
    if (
        "イッテQ" in title
        and target_start <= program_start
        and program_end <= target_end
    ):
        print(f"✅ Matched: {title}")
        filtered.append(p)

# 結果保存
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)