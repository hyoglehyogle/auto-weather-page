import requests
from bs4 import BeautifulSoup, NavigableString
from datetime import datetime, timedelta

def scrape_land_weather():
    url = 'https://www.weather.go.kr/w/weather/forecast/mid-term.do'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # '육상날씨'부터 '최저/최고기온' 전까지 추출
    content = soup.find('div', class_='tab-menu-cont')
    output_html = ""
    capture = False

    for tag in content.find_all(['h3', 'div']):
        if tag.name == 'h3' and '육상날씨' in tag.text:
            capture = True
            output_html += str(tag)
            continue
        if capture:
            if tag.name == 'h3' and '최저/최고기온' in tag.text:
                break

            # ✅ 날씨 텍스트 → 이모지 아이콘 매핑
            icon_map = {
                "맑음": "☀️",
                "흐림": "⛅️",
                "구름많음": "☁️",
                "흐리고 비": "🌧️",
                "비": "☔️",
                "눈": "❄️",
                "황사": "🌫️"
            }

            for text, icon in icon_map.items():
                if tag.string and text in tag.string:
                    tag.string.replace_with(tag.string.replace(text, icon))
                elif text in tag.decode_contents():
                    tag.clear()
                    tag.append(NavigableString(tag.decode_contents().replace(text, icon)))

            output_html += str(tag)

    # 오늘 날짜 포함한 제목 생성 (한국 시간 기준)
    date_str = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y년 %m월 %d일 %H:%M 기준")

    final_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>주간 육상 날씨</title>
    </head>
    <body>
        <h2>주간 육상 날씨</h2>
        <p><strong>최종 업데이트:</strong> {date_str}</p>
        {output_html}
    </body>
    </html>
    """

    # HTML 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    scrape_land_weather()
