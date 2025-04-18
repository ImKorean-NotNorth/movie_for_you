from pandas.io.sas.sas_constants import sas_datetime_formats
from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By # selenium 세팅
from selenium.webdriver.common.keys import Keys # 키를 자동으로 누르기위해 필요
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager #구글 초기설정 2개
import pandas as pd
import re
import time
import datetime

# 클래스 매서드가 아니라 인스턴스 매서드이기 때문
# ChromeOptions() 객체를 생성한 후, add_experimental_option()을 호출하면 정상적으로 동작합니다.
#option = ChromeOptions()  # 객체 생성
#option.add_experimental_option('prefs', {'profile.default_content_setting_values.notifications': 1})
#되긴하는데 잘안돼..

Options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'

Options.add_argument('user_agent=' + user_agent)
Options.add_argument('long=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=Options)

#===============================================================================================
df_titles = pd.DataFrame()
Titles = []
Reviews = []



#
def open_in_new_tab(driver, element):
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
    driver.switch_to.window(driver.window_handles[-1])

def srolling():
    for _ in range(10):  # 50번 페이지 다운 시도
        # 페이지의 body 요소를 찾아서 end 키를 보냄
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)
#
#
# # for z in range(1):
#
# df_titles = pd.DataFrame()
# url = 'https://laftel.net/finder'
# body = driver.find_element(By.TAG_NAME, "body")
# driver.get(url)
# time.sleep(2)
#
# sleep_sec = 3
#
# # 인기 순 버튼
# button_CSS_pop = '#root > div.sc-f0aad20d-0.cJKdpk > div.sc-314e188f-0.hqsXVO > div.sc-314e188f-2.hVHfbj > div > div > div > div.simplebar-wrapper > div.simplebar-mask > div > div > div > div.sc-b650993-1.dPuSyZ > div.sc-42a3c8f1-0.eiatWD > div > div > div.sc-29d1736d-0.fkHAgS > div > div'
# button = driver.find_element(By.CSS_SELECTOR, button_CSS_pop)
# driver.execute_script("arguments[0].scrollIntoView(true);", button)
# time.sleep(1)
# # JavaScript로 클릭 시도
# driver.execute_script("arguments[0].click();", button)
# print("인기순 버튼 클릭")
# time.sleep(2)  # 페이지 로딩 대기
#
# #리뷰 많은순 버튼
# button_CSS_review = '#root > div.sc-f0aad20d-0.cJKdpk > div.sc-314e188f-0.hqsXVO > div.sc-314e188f-2.hVHfbj > div > div > div > div.simplebar-wrapper > div.simplebar-mask > div > div > div > div.sc-b650993-1.dPuSyZ > div.sc-42a3c8f1-0.eiatWD > div > div > div.sc-29d1736d-0.fkHAgS > div.sc-29d1736d-3.bblvNc > div:nth-child(6) > div.sc-29d1736d-8.fDdkop'
# button = driver.find_element(By.CSS_SELECTOR, button_CSS_review)
# driver.execute_script("arguments[0].scrollIntoView(true);", button)
# time.sleep(1)
# # JavaScript로 클릭 시도
# driver.execute_script("arguments[0].click();", button)
# print("리뷰순 버튼 클릭")
# time.sleep(2)  # 페이지 로딩 대기
#
# # end 전 옆 배경 누르기
# button_xpath_background = '//*[@id="root"]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div'
# driver.find_element(By.XPATH, button_xpath_background).click()
# time.sleep(sleep_sec)
#
# srolling()
#time.sleep(5)

driver.get("https://laftel.net/finder")
body = driver.find_element(By.TAG_NAME, "body")
time.sleep(1)

for i in range(1, 200):
    try:
        TitleTap_Xpath = f'//*[@id="root"]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/a[{i}]/div'
        driver.find_element(By.XPATH, TitleTap_Xpath).click()
        time.sleep(1)

        ReviewsTap_Xpath = '//*[@id="item-tab-view"]/div[1]/div/div/div[1]/a[2]'
        driver.find_element(By.XPATH, ReviewsTap_Xpath).click()
        time.sleep(1)



        [(driver.find_element(By.XPATH, '//*[@id="item-tab-view"]').click(),
          time.sleep(0.5), body.send_keys(Keys.END), time.sleep(0.5)) for _ in range(4)] # 리뷰창 스크롤 4번

        # ✅ for j 루프 들여쓰기 수정
        for j in range(1, 50):
            try:

                Reviews_xpath = f'//*[@id="item-tab-view"]/div[2]/div/section[2]/ul/div[{j}]/li/article'
                Review = driver.find_element(By.XPATH, Reviews_xpath).text
                Review = re.compile('[^가-힣 ]').sub('', Review)  # 한글만 남김
                Reviews.append(Review)
                print(Review)
                time.sleep(0.5)

            except NoSuchElementException:
                print(f"[{j}] 번째 없음 건너뜀")
                continue  # 다음 j 값으로 넘어감

        body.send_keys(Keys.ESCAPE)  # ESC 키 입력 (닫기)
        time.sleep(1)

    except NoSuchElementException:
        print(f"[{i}] 번째 없음 건너뜀")
        continue  # 다음 i 값으로 넘어감

print("Finish")
print(Reviews)


# try:
#     review = driver.find_element(By.XPATH, reviews_xpath).text
#     title = re.compile('[^가-힣 ]').sub('', title)
#     # 그걸 리스트에 추가
#     titles.append(title)





# for i in range(1, 50):
#
#
# driver.find_element(By.CSS_SELECTOR, #CSS 주소
#                    "#item-tab-view > div.sc-f1e3e87e-2.evwnQw > div > div > div.sc-f1e3e87e-5.dvbprG > a:nth-child(2)").click()
#
# body = driver.find_element(By.TAG_NAME, 'body')
# content_body = driver.find_element(By.XPATH, "//*[@id='content__body']")
#
#
#
# for i in range(3, 53):  # 1부터 50까지
#     try:
#         # 영화 제목 가져오기
#         movie_title = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR,
#                  "#contents > div.movie-info-container > div.content-info > div.movie-header-area > div.movie-title-wrap > h2")
#             )
#         ).text
#
#         # 리뷰 제목 가져오기 (세 번째 리뷰 항목)
#         review_title = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR,
#                  f"#contents > div.review.tab-item > section.review-list-section > div > article:nth-child({i}) > div.review-item__contents > a > h5")
#             )
#         ).text
#
#         # 제목들을 리스트에 추가
#         movie_titles.append(movie_title)
#         review_titles.append(review_title)
#
#         print(f"{i}: 영화 제목: {movie_title}, 리뷰 제목: {review_title}")
#     except Exception as e:
#         print(f"{i}: 오류 발생 (오류: {e})")
#         driver.back()
#         time.sleep()
#
# //*[@id="contents"]/div[5]/section[2]/div/article[40]/div[3]/a/h5
# //*[@id="contents"]/div[5]/section[2]/div/article[60]/div[3]/a/h5
#
# 등급설정 말고는 XPATH 가능 XPATH는 '' celector는 "" 왜 안되고 왜 되는지 모르겠음
#
#
# //*[@id="contents"]/div/div/div[3]/div[2]/div[1]/a/div/div[1]/div[1]/img
# driver.find_element(By.CSS_SELECTOR,
#                     "#").click()
#
#
#
# driver.find_element(By.XPATH, '//*[@id="contents"]/section/div[3]/div/div/div[6]/button/span').click()
# 왜 위에는 강제실행을 해야하지?,,
#
#
#
# 이 리뷰에는 스포일러가 포함되어 있습니다. x
# div/p 가 포함되면 내용 삭제
#
# df_titles.to_csv(f'./crawling_data/naver_headline_news_2_3_{datetime.datetime.now().strftime("%y%m%d")}.csv',
#                  index=False)
