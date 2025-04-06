# check_program.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime, time

def check_programs_on_sunday_evening(url, keyword=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    program_items = soup.find_all('li', class_='sc-future')
    results = []

    for item in program_items:
        start_attr = item.get('s')  # 開始時刻（形式：202504061958）
        if not start_attr:
            continue

        start_dt = datetime.strptime(start_attr, "%Y%m%d%H%M")

        # 日曜日かつ19:00〜21:00の時間帯に限定
        if start_dt.weekday() == 6 and time(19, 0) <= start_dt.time() < time(21, 0):
            title_tag = item.find('p', class_='program_title')
            detail_tag = item.find('p', class_='program_detail')
            title = title_tag.get_text(strip=True) if title_tag else ''
            detail = detail_tag.get_text(strip=True) if detail_tag else ''

            if keyword is None or keyword in title:
                results.append({
                    'start_time': start_dt.strftime("%Y-%m-%d %H:%M"),
                    'title': title,
                    'detail': detail
                })

    return results

# 実行部分
if __name__ == "__main__":
    url = "https://bangumi.org/epg/td?ggm_group_id=67"
    keyword = "イッテQ"
    matched_programs = check_programs_on_sunday_evening(url, keyword)

    if matched_programs:
        for program in matched_programs:
            print("---- 番組 ----")
            print("開始時間:", program['start_time'])
            print("タイトル:", program['title'])
            print("詳細:", program['detail'])
    else:
        print("日曜19:00〜21:00の間に該当番組は見つかりませんでした。")
