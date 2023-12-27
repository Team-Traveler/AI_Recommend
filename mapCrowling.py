import pandas as pd # 표 형식의 데이터를 다룰 수 있는 pandas를 pd라고 줄여서 불러옵니다
from selenium import webdriver # 크롬 창을 조종하기 위한 모듈입니다
from selenium.webdriver.common.by import By # 웹사이트의 구성요소를 선택하기 위해 By 모듈을 불려옵니다
from selenium.webdriver.support.ui import WebDriverWait # 웹페이지가 전부 로드될때까지 기다리는 (Explicitly wait) 기능을 하는 모듈입니다
from selenium.webdriver.support import expected_conditions as EC # 크롬의 어떤 부분의 상태를 확인하는 모듈입니다
import time # 정해진 시간만큼 기다리게 하기 위한 패키지입니다
import json
import requests
from flask import Flask, request


def trans_address(addr):
    apiurl = "https://api.vworld.kr/req/address?"
    params = {
        "service": "address",
        "request": "getcoord",
        "crs": "epsg:4326",
        "address": addr,
        "format": "json",
        "type": "road",
        "key": "D5418F99-29C7-345E-8A31-65594EA9383E"
    }
    response = requests.get(apiurl, params=params)
    if response.status_code == 200:
        data = response.json()
        status = data['response']['status']
        if status == 'OK':
            latitude = float(data['response']['result']['point']['y'])
            longitude = float(data['response']['result']['point']['x'])
            print('위경도:', latitude, longitude)
            return [latitude, longitude]
        else:
            return 0
    else:
        return 0


app = Flask(__name__)


@app.route('/', methods=['GET'])
def recomm_restaurant():
    search_keyword = request.args.get('keyword')
    # search_keyword = '서울 맛집'

    # 창 숨기는 옵션 추가
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = driver = webdriver.Chrome(options=options)
    driver.get(f"https://maps.google.com/search?sca_esv=586327572&tbs=lf:1,lf_ui:9&tbm=lcl&q={search_keyword}")
    try:
        element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "SDkEP")))
    finally:
        pass

    res = pd.DataFrame()
    empty = '#search'  # 크롤링할 데이터가 있는 영역 중, 빈 공간을 입력해 뒀습니다

    check = 10
    count = 0

    while check:
        places = driver.find_elements(By.CLASS_NAME, "rllt__details")
        print(len(places))
        for place in places:
            nm = place.find_element(By.CLASS_NAME, "OSrXXb").text.strip()
            score = place.find_element(By.CLASS_NAME, "yi40Hd.YrbPuc").text.strip()
            address = place.find_element(By.XPATH, './div[3]').text.strip()

            if nm != []:  # 이름이 비어있으면 아무것도 안하도록
                addr = trans_address(address)

            if addr:
                res = pd.concat([res, pd.DataFrame([nm, addr, score]).T])  # res 데이터프레임에 차곡차곡 쌓아줍니다
                count = count + 1
                if count == 20:
                    check = 0
                    break
            print(count, check)

        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pnnext")))
        # 다음 버튼 클릭
        next_button.click()
        time.sleep(3)

    res.columns = ['name', 'addr', 'score']
    res = res.sort_values('score', ascending=False)
    print(res)
    data_df = pd.DataFrame(res)
    data_js = data_df.values.tolist()
    data = json.dumps(list(data_js), ensure_ascii=False).encode('utf8')
    return data


if __name__=='__main__':
 app.run(host='0.0.0.0', port=8000, debug=True)
