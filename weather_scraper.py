import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
            output_html += str(tag)

    # 오늘 날짜 포함한 제목 생성
    date_str = datetime.today().strftime("%Y년 %m월 %d일 %H:%M 기준")
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
