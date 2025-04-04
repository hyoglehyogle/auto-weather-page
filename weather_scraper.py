import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re  # 숫자% 제거용

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

            # ✅ 아이콘 매핑
            icon_map = {
                "맑음": "☀️",
                "흐림": "⛅️",
                "구름많음": "☁️",
                "흐리고 비": "🌧️",
                "비": "☔️",
                "눈": "❄️",
                "황사": "🌫️"
            }

            # ✅ <td> 안에서 아이콘 치환 + 숫자% 제거
            for td in tag.find_all("td"):
                text = td.text

                # 아이콘 치환
                for word, icon in icon_map.items():
                    if word in text:
                        text = text.replace(word, icon)

                # 숫자% 제거
                text = re.sub(r'\d+%', '', text).strip()

                td.string = text

            output_html += str(tag)

    # ✅ 한국 시간 기준으로 최종 업데이트 시간 표시
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

    # ✅ index.html로 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    scrape_land_weather()
