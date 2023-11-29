
import pandas as pd # 표 형식의 데이터를 다룰 수 있는 pandas를 pd라고 줄여서 불러옵니다
from selenium import webdriver # 크롬 창을 조종하기 위한 모듈입니다
from selenium.webdriver.common.by import By # 웹사이트의 구성요소를 선택하기 위해 By 모듈을 불려옵니다
from selenium.webdriver.support.ui import WebDriverWait # 웹페이지가 전부 로드될때까지 기다리는 (Explicitly wait) 기능을 하는 모듈입니다
from selenium.webdriver.support import expected_conditions as EC # 크롬의 어떤 부분의 상태를 확인하는 모듈입니다
import time # 정해진 시간만큼 기다리게 하기 위한 패키지입니다

search_keyword = '서울 맛집'

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

for i in range(10, 31):
    nm = ['NA']
    addr = ['NA']
    score = ['NA']

    driver.find_element(By.CSS_SELECTOR, empty)
    nm_elements = driver.find_elements(By.CSS_SELECTOR,
                                        f'#tsuid_{i} > div.uMdZh.tIxNaf > div > div > a.vwVdIc.wzN8Ac.rllt__link.a-no-hover-decoration > div > div > div.dbg0pd > span')

    driver.find_element(By.CSS_SELECTOR, empty)
    addr_elements = driver.find_elements(By.CSS_SELECTOR,
                                          f'#tsuid_{i} > div.uMdZh.tIxNaf > div > div > a.vwVdIc.wzN8Ac.rllt__link.a-no-hover-decoration > div > div > div:nth-child(3)')

    driver.find_element(By.CSS_SELECTOR, empty)
    score_elements = driver.find_elements(By.CSS_SELECTOR,
                                         f'#tsuid_{i} > div.uMdZh.tIxNaf > div > div > a.vwVdIc.wzN8Ac.rllt__link.a-no-hover-decoration > div > div > div:nth-child(2) > span > span > span.yi40Hd.YrbPuc')

    if nm_elements != []:  # 이름이 비어있으면 아무것도 안하도록
        nm = nm_elements[0].text
        addr = addr_elements[0].text
        score = score_elements[0].text

        res = pd.concat([res, pd.DataFrame([nm, addr, score]).T])  # res 데이터프레임에 차곡차곡 쌓아줍니다

res.columns = ['name', 'addr', 'score']
res = res.sort_values('score', ascending=False)
print(res)

