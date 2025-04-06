import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta

OUTPUT_FILE = "data/program_data.json"
GROUP_ID = 67

def get_next_sunday():
    today = datetime.today()
    days_ahead = 6 - today.weekday()  # weekday: 0=Mon, ..., 6=Sun
    if days_ahead <= 0:
        days_ahead += 7
    next_sunday = today + timedelta(days=days_ahead)
    return next_sunday.strftime("%Y%m%d")

def fetch_programs():
    date_str = get_next_sunday()
    url = f"https://bangumi.org/epg/td?broad_cast_date={date_str}&ggm_group_id={GROUP_ID}"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    programs = []

    for li in soup.select("li.sc-future"):
        start_raw = li.get("s")
        end_raw = li.get("e")
        if not start_raw or not end_raw:
            continue

        try:
            start_dt = datetime.strptime(start_raw, "%Y%m%d%H%M")
            end_dt = datetime.strptime(end_raw, "%Y%m%d%H%M")
        except ValueError:
            continue

        title_tag = li.select_one("p.program_title")
        detail_tag = li.select_one("p.program_detail")
        if not title_tag:
            continue

        programs.append({
            "title": title_tag.text.strip(),
            "detail": detail_tag.text.strip() if detail_tag else "",
            "start_time": start_dt.strftime("%Y-%m-%d %H:%M"),
            "end_time": end_dt.strftime("%Y-%m-%d %H:%M")
        })

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(programs, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_programs()
