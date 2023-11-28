
import pandas as pd # 표 형식의 데이터를 다룰 수 있는 pandas를 pd라고 줄여서 불러옵니다
from selenium import webdriver # 크롬 창을 조종하기 위한 모듈입니다
from selenium.webdriver.common.by import By # 웹사이트의 구성요소를 선택하기 위해 By 모듈을 불려옵니다
from selenium.webdriver.support.ui import WebDriverWait # 웹페이지가 전부 로드될때까지 기다리는 (Explicitly wait) 기능을 하는 모듈입니다
from selenium.webdriver.support import expected_conditions as EC # 크롬의 어떤 부분의 상태를 확인하는 모듈입니다
import time # 정해진 시간만큼 기다리게 하기 위한 패키지입니다

driver = driver = webdriver.Chrome() # 웹 드라이버를 설치하고, 조종할 수 있는 크롬 창을 실행합니다
driver.get("https://map.naver.com/v5/search/서울 맛집")

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
    ) # 네이버 지도의 검색창은 "input_search" 라는 클래스 이름으로 설정되어 있습니다
finally:
    pass

element = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it("searchIframe"))

res = pd.DataFrame()  # 결과 파일은 판다스 데이터프레임으로 입력할겁니다
empty = '#_pcmap_list_scroll_container'  # 크롤링할 데이터가 있는 영역 중, 빈 공간을 입력해 뒀습니다

driver.find_element(By.CSS_SELECTOR, empty)  # 이렇게 find_element 함수만 사용해 놓으면 그 영역이 인식되더라고요

for i in range(1, 51):
    print(i)
    nm = ['NA']
    addr = ['NA']

    driver.find_element(By.CSS_SELECTOR, empty)

    nm_elements = driver.find_elements(By.CSS_SELECTOR,
                                        f'#_pcmap_list_scroll_container > ul > li:nth-child({i}) > div.CHC5F > a > div > div > span.TYaxT')
    # nm_elements += driver.find_elements(By.CSS_SELECTOR,
    #                                      f'#_pcmap_list_scroll_container > ul > li:nth-child({i}) > div:nth-child(1) > div > a:nth-child(1) > div > div > span:nth-child(1)')

    driver.find_element(By.CSS_SELECTOR, empty)

    addr_elements = driver.find_elements(By.CSS_SELECTOR,
                                          f'#_pcmap_list_scroll_container > ul > li:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div > div > div')
    addr_elements += driver.find_elements(By.CSS_SELECTOR,
                                           f'#_pcmap_list_scroll_container > ul > li:nth-child({i}) > div:nth-child(1) > div > div > div > span > a > span:nth-child(1)')

    if nm_elements:  # 수정: nm_elements가 비어있는지 확인
        addr = addr_elements[0].text
        print(nm_elements[0].text, addr)
        if any(i in addr for i in ['서울']):
            res = pd.concat([res, pd.DataFrame([nm_elements[0].text, addr]).T])
            res.to_csv('./res_naver.csv', index=False)