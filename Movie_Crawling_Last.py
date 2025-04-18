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

category = ['Titles', 'Review']

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

first_ten_flag = 0 # flag 세우기
# for z in range(1):

df_titles = pd.DataFrame()
for x in range(4, 5):
    driver.get("https://ridibooks.com/category/bestsellers/6050?page={}&period=steady&adult_exclude=y".format(x))
    body = driver.find_element(By.TAG_NAME, "body")
    time.sleep(1)

    sleep_sec = 2

    srolling()
    # 홈키 클릭
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
    time.sleep(sleep_sec)

    # for i in range(1, 60):
    for i in range(1, 21):
        time.sleep(sleep_sec)
        titles = []
        reviews = []
        try:
            TitleTap_Xpath = f'//*[@id="__next"]/main/div/section/ul[3]/li[{i}]/div/div[3]/div/div[1]/a'

            # 새 탭에서 책 열기
            element = driver.find_element(By.XPATH, TitleTap_Xpath)
            open_in_new_tab(driver, element)
            print(i)
            time.sleep(sleep_sec)

            # 타이틀 추출
            title_xpath = '//*[@id="ISLANDS__Header"]/div/div/div/div[2]/h1'
            try:
                title = driver.find_element(By.XPATH, title_xpath).text
                title = re.sub('"', '', title)  # 모든 종류의 큰따옴표 제거
                titles.append(title)
                print(f"현재 작품 타이틀: {title} 입니다.")
            except Exception as e:
                print(f"타이틀 추출 중 오류: {e}")
                # 현재 탭 닫기
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            # 리뷰 갯수 구하기
            review_cnt = '//*[@id="detail_review"]/div[3]/button[2]/span[2]'
            review_cnt = driver.find_element(By.XPATH, review_cnt).text
            print(review_cnt + '개 입니다.')

            # 문자열에서 숫자만 추출하여 정수로 변환
            review_cnt = int(re.sub(r'\D', '', review_cnt))
            print(f"리뷰 개수: {review_cnt}개")

            try:
                # 리뷰 개수 확인
                if review_cnt < 11:
                    print(f"리뷰 개수 {review_cnt}개: 다음 작품으로 넘어갑니다.")
                    print(f"현재 작품 타이틀: {title}")
                    # 현재 탭(새로 열린 탭) 닫기
                    driver.close()

                    # 원래 탭으로 돌아가기
                    driver.switch_to.window(driver.window_handles[0])
                    print(f"현재 작품 타이틀: {title} 탭 닫기")
                    time.sleep(5)
                    continue
                else:
                    pass
            except Exception as e:
                print(f'리뷰 개수 확인 중 오류 발생: {e}')
                continue

            try:

                button_xpath_all = '//*[@id="detail_review"]/div[3]/button[2]'  # 최신 리뷰 버튼
                driver.find_element(By.XPATH, button_xpath_all).click()  # 클릭
                time.sleep(sleep_sec)
                print('전체 탭 클릭')
            except Exception as e:
                print(f"최신 탭 클릭 중 예외 발생: {e}")
                break

            # 더보기 클릭
            button_xpath_more = '//*[@id="detail_review"]/div[5]/button/span'

            for _ in range(4):  # 4번 페이지 더보기 시도
                try:
                    # 페이지의 body 요소를 찾아서 더보기 버튼 클릭
                    driver.find_element(By.XPATH, button_xpath_more).click()
                    time.sleep(sleep_sec)
                    print('더보기 완료')
                except Exception as e:
                    print(f"예외 발생: {e}")
                    break  # for문 즉시 종료
            print('더보기 4번 완료')
            # input("멈춤")
            #  for j 루프 들여쓰기 수정
            for j in range(1, 50):
                try:
                    if j <= 10:
                        if first_ten_flag == 0:
                            review_xpath = '//*[@id="detail_review"]/ul/li[{}]/div[2]/p'.format(j)
                            review = driver.find_element(By.XPATH, review_xpath).text
                            if j == 10:
                                first_ten_flag = 1
                        else:
                            review_CSS_selector = '#detail_review > ul > li:nth-child({}) > div.rigrid-3s6awr > p'.format(j)
                            review = driver.find_element(By.CSS_SELECTOR, review_CSS_selector).text
                    else:
                        review_CSS_selector = '#detail_review > ul > li:nth-child({}) > div.rigrid-1hjvtyt-Jg > p'.format(j)
                        review = driver.find_element(By.CSS_SELECTOR, review_CSS_selector).text
                    review = re.compile('[^가-힣 ]').sub('', review)  # 한글만 남김
                    reviews.append(review)
                    print(review)
                    # time.sleep(0.5)

                except NoSuchElementException:
                    print(f"[{j}] 번째 없음 건너뜀")
                    continue  # 다음 j 값으로 넘어감

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
            'Title': [title] * len(reviews),
            'Review': reviews
        }
        df_section = pd.DataFrame(data)
        df_titles = pd.concat([df_titles, df_section], ignore_index=True)

print(df_titles.head())
df_titles.info()
df_titles.to_csv('./crawling_data/ridi_{}_{}_v4.csv'.format(400,
datetime.datetime.now().strftime('%Y%m%d')), index=False) # 나노second단위 받은 시간으로 오늘 날짜로 바꿔서 저장

time.sleep(10)
driver.close()

