from selenium import webdriver # 모든 브라우저
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException


options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')
options.add_argument("--blink-settings=imagesEnabled=false") # 이미지 비활성화


service = ChromeService(executable_path=ChromeDriverManager().install()) # 브라우저 install
driver = webdriver.Chrome(service=service, options=options)

category = ['Titles', 'Reviews']

def open_in_new_tab(driver, element):
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
    driver.switch_to.window(driver.window_handles[-1])

def srolling():
    # for _ in range(10):  # 50번 페이지 다운 시도
    for _ in range(5):  # 50번 페이지 다운 시도
        # 페이지의 body 요소를 찾아서 end 키를 보냄
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)


# for z in range(1):

df_titles = pd.DataFrame()
Titles = []
Reviews = []
driver.get("https://laftel.net/finder")
body = driver.find_element(By.TAG_NAME, "body")
time.sleep(1)

sleep_sec = 2

# 인기 순 버튼
button_CSS_pop = '#root > div.sc-f0aad20d-0.cJKdpk > div.sc-314e188f-0.hqsXVO > div.sc-314e188f-2.hVHfbj > div > div > div > div.simplebar-wrapper > div.simplebar-mask > div > div > div > div.sc-b650993-1.dPuSyZ > div.sc-42a3c8f1-0.eiatWD > div > div > div.sc-29d1736d-0.fkHAgS > div > div'
button = driver.find_element(By.CSS_SELECTOR, button_CSS_pop)
driver.execute_script("arguments[0].scrollIntoView(true);", button)
time.sleep(1)
# JavaScript로 클릭 시도
driver.execute_script("arguments[0].click();", button)
print("인기순 버튼 클릭")
time.sleep(2)  # 페이지 로딩 대기

#리뷰 많은순 버튼
button_CSS_review = '#root > div.sc-f0aad20d-0.cJKdpk > div.sc-314e188f-0.hqsXVO > div.sc-314e188f-2.hVHfbj > div > div > div > div.simplebar-wrapper > div.simplebar-mask > div > div > div > div.sc-b650993-1.dPuSyZ > div.sc-42a3c8f1-0.eiatWD > div > div > div.sc-29d1736d-0.fkHAgS > div.sc-29d1736d-3.bblvNc > div:nth-child(6) > div.sc-29d1736d-8.fDdkop'
button = driver.find_element(By.CSS_SELECTOR, button_CSS_review)
driver.execute_script("arguments[0].scrollIntoView(true);", button)
time.sleep(1)
# JavaScript로 클릭 시도
driver.execute_script("arguments[0].click();", button)
print("리뷰순 버튼 클릭")
time.sleep(2)  # 페이지 로딩 대기

# end 전 옆 배경 누르기
button_xpath_background = '//*[@id="root"]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div'
driver.find_element(By.XPATH, button_xpath_background).click()
time.sleep(sleep_sec)

srolling()
# 홈키 클릭
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
time.sleep(sleep_sec)

for i in range(1, 200):
# for i in range(1, 3):
    try:
        TitleTap_Xpath = f'//*[@id="root"]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/a[{i}]/div'
        # driver.find_element(By.XPATH, TitleTap_Xpath).click()
        # time.sleep(sleep_sec)

        # 새 탭에서 책 열기
        element = driver.find_element(By.XPATH, TitleTap_Xpath)
        open_in_new_tab(driver, element)
        print(i)
        time.sleep(sleep_sec)

        # 타이틀 추출
        title_xpath = '//*[@id="item-modal"]/div[1]/div[2]/div/header/h1'
        try:
            title = driver.find_element(By.XPATH, title_xpath).text
            title = re.sub('"', '', title)  # 모든 종류의 큰따옴표 제거
            Titles.append(title)
            print(f"현재 작품 타이틀: {title} 입니다.")
        except Exception as e:
            print(f"타이틀 추출 중 오류: {e}")
            # 현재 탭 닫기
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue

        ReviewsTap_Xpath = '//*[@id="item-tab-view"]/div[1]/div/div/div[1]/a[2]'
        driver.find_element(By.XPATH, ReviewsTap_Xpath).click()
        time.sleep(sleep_sec)

        # [(driver.find_element(By.XPATH, '//*[@id="item-tab-view"]').click(),
        #   time.sleep(0.5), body.send_keys(Keys.END), time.sleep(0.5)) for _ in range(4)] # 리뷰창 스크롤 4번
        srolling()

        #  for j 루프 들여쓰기 수정
        for j in range(1, 50):
            try:
                Reviews_xpath = f'//*[@id="item-tab-view"]/div[2]/div/section[2]/ul/div[{j}]/li/article'
                Review = driver.find_element(By.XPATH, Reviews_xpath).text
                Review = re.compile('[^가-힣 ]').sub('', Review)  # 한글만 남김
                Reviews.append(Review)
                print(Review)
                # time.sleep(0.5)

            except NoSuchElementException:
                print(f"[{j}] 번째 없음 건너뜀")
                continue  # 다음 j 값으로 넘어감
        # input("멈춤")
        # body.send_keys(Keys.ESCAPE)  # ESC 키 입력 (닫기)
        # time.sleep(sleep_sec)
        # 현재 탭(새로 열린 탭) 닫기
        driver.close()

        # 원래 탭으로 돌아가기
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(sleep_sec)

    except NoSuchElementException:
        print(f"[{i}] 번째 없음 건너뜀")
        continue  # 다음 i 값으로 넘어감

    # 각 영화마다 제목과 리뷰를 매칭하여 데이터프레임 생성
    data = {
        'Titles': [title] * len(Reviews),  # 리뷰 개수만큼 제목 반복
        'Reviews': Reviews
    }
    df_section = pd.DataFrame(data)
    df_titles = pd.concat([df_titles, df_section], ignore_index=True)

print(df_titles.head())
df_titles.info()
df_titles.to_csv('./crawling_data/laftel_{}_{}.csv'.format(400,
datetime.datetime.now().strftime('%Y%m%d')), index=False) # 나노second단위 받은 시간으로 오늘 날짜로 바꿔서 저장

time.sleep(10)
driver.close()