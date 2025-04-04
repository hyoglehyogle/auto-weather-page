import requests
from bs4 import BeautifulSoup
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

     # ✅ 여기서 태그 안 텍스트에 아이콘 치환!
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
                tag.append(BeautifulSoup(tag.decode_contents().replace(text, icon), 'html.parser'))

            output_html += str(tag)

    # 오늘 날짜 포함한 제목 생성
    date_str = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y년 %m월 %d일 %H:%M 기준")
    final_html = f"""
    <html>
    <head>
    </head>
    <body>
        <h2>주간 육상 날씨</h2>
        <p>{date_str}</p>
        {output_html}
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    scrape_land_weather()
