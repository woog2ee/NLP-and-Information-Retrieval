import re
import sys
import time
import pandas as pd
from tqdm import tqdm
from selenium import webdriver



def get_daumnews_info(date):
    # 크롤링 정보    
    list_all_headline = []     # 뉴스 제목
    list_all_address  = []     # 뉴스 주소
    list_all_content  = []     # 뉴스 본문
    list_all_newsinfo = []     # 뉴스 날짜/카테고리
    categories = ['society/affair', 'society/others', 'society/labor', 'politics/administration', 'politics/dipdefen', 'economic/consumer']
    
    
    # 드라이버 실행
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--incognito')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('chromedriver.exe', options=options)     
    driver.implicitly_wait(3)
    
    
    # 카테고리를 돌며 크롤링
    for category in categories:
        list_headline = []
        list_address  = []
        list_content  = []
        list_newsinfo = []
        page = 0
        top_headline = ''             # 페이지내 맨위 뉴스 제목
        top_headline_flag = False     # 다음 페이지 맨위 뉴스제목이 기존 페이지 맨위 뉴스제목과 다름  

        
        # 제목, 주소 크롤링
        while True:
            try:
                # 페이지 이동
                page += 1
                driver.get(f'https://news.daum.net/breakingnews/{category}?page={page}&regDate={date}')
                time.sleep(1)        

                
                # 크롤링
                page_news = driver.find_elements_by_css_selector('#mArticle > div > ul > li > div > strong > a')
                cnt = 0
                for news in page_news:
                    # 다음 페이지 맨위 뉴스제목이 기존 페이지 맨위 뉴스제목과 같으면 해당 카테고리 종료
                    if cnt == 0 and news.text == top_headline:
                        top_headline_flag = True
                        break
                    
                    # 페이지내 맨위 뉴스제목 저장
                    if cnt == 0:
                        top_headline = news.text
                    
                    # 뉴스 정보 저장                    
                    if (cnt != 0) and (news.text in list_headline): continue
                    if (cnt != 0) and ('[' in news.text): continue  
                    list_headline.append(news.text)
                    list_address.append(news.get_attribute('href'))
                    list_newsinfo.append(str(date) + '/' + category)
                    cnt += 1

                    
                # 다음 페이지 맨위 뉴스제목이 기존 페이지 맨위 뉴스제목과 같으면 해당 카테고리 종료
                if top_headline_flag == True:
                    break
            except:
                pass
            
            
        # 본문 크롤링
        drop_idx = []
        cnt = 0
        for address in tqdm(list_address):
            try:
                # 주소 이동
                driver.get(address)
                time.sleep(1)
                
                
                # 뉴스 본문 저장
                cur_content = ''
                contents = driver.find_elements_by_css_selector('#harmonyContainer > section')
                for content in contents:
                    cur_content += content.text
                list_content.append(cur_content)
            except:
                drop_idx.append(cnt)     # 본문이 크롤링되지 않는 경우
                pass
            cnt += 1


        # 본문 결측치 관련 정보 제거
        for i in range(len(drop_idx)):
            idx = drop_idx[len(drop_idx)-1-i]
            list_headline.pop(idx)
            list_address.pop(idx)
            list_newsinfo.pop(idx)


        # 카테고리별 정보 통합
        list_all_headline += list_headline
        list_all_address += list_address
        list_all_content += list_content
        list_all_newsinfo += list_newsinfo



    driver.quit()
    daumnews_info = pd.DataFrame({'제목': list_all_headline, '주소': list_all_address, '본문': list_all_content, '날짜/카테고리': list_all_newsinfo})      
    return daumnews_info



def preprocess_content(text):    
    # 괄호 안 제거
    text = re.sub(r'\([^)]*\)', '', text)    
    text = re.sub(r'\{[^}]*\}', '', text)
    text = re.sub(r'\[[^]]*\]', '', text)
    text = re.sub(r'\<[^>]*\>', '', text)
    
    # 공백 제거
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s+', '', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'\t', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    
    # 이메일 제거
    text = re.sub(r'[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+','', text)
    
    # url 제거
    text = re.sub(r'http[s]?://(?:[\t\n\r\f\v]|[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text) 
    text = re.sub(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{2,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', '', text)      
    
    # 사진 정보 제거
    text = re.sub(r'사진=[^\s]*[\s]*[캡쳐]*', '', text)
    
    # 기호 글자 조합 제거
    text = re.sub(r'▲[^\s]+[\s]*[^\s]+[%]*', '', text)
    text = re.sub(r'[\s]+', ' ', text)
    text = re.sub(r'▶제보는 카톡 [a-zA-Z]+', '', text)
    
    # 기자명 제거
    text = re.sub(r'[^\s]{3,4}\s기자', '', text)
    text = re.sub(r'[ㄱ-ㅎ|ㅏ-ㅣ|가-힣\s]+기자' ,'', text)
    
    # 따옴표 제거
    text = re.sub(r'\'', '', text)
    
    # 특수문자 제거
    text = re.sub(r'[^0123456789ㄱ-ㅎ|ㅏ-ㅣ|가-힣a-zA-Z\s.,!?]', '', text)

    return text.strip()



if __name__ == "__main__":       
    # 크롤링 진행
    date = sys.argv[1]
    print(f'<Crawling> {date} 일자 다음뉴스 크롤링을 시작합니다.')
    globals()[f'daumnews_{date}'] = get_daumnews_info(date)
    

    # 전처리 후 저장
    globals()[f'daumnews_{date}']['본문'] = globals()[f'daumnews_{date}']['본문'].apply(preprocess_content)
    globals()[f'daumnews_{date}'].to_csv(f'./다음뉴스_{date}_크롤링.csv', encoding='utf-8-sig', index=False)
    print(f'<Preprocessing> {date} 일자 다음뉴스 전처리 후 저장을 완료했습니다.')



    # 크롤링 진행
    date = sys.argv[2]
    print(f'<Crawling> {date} 일자 다음뉴스 크롤링을 시작합니다.')
    globals()[f'daumnews_{date}'] = get_daumnews_info(date)
    

    # 전처리 후 저장
    globals()[f'daumnews_{date}']['본문'] = globals()[f'daumnews_{date}']['본문'].apply(preprocess_content)
    globals()[f'daumnews_{date}'].to_csv(f'./다음뉴스_{date}_크롤링.csv', encoding='utf-8-sig', index=False)
    print(f'<Preprocessing> {date} 일자 다음뉴스 전처리 후 저장을 완료했습니다.')



    # 크롤링 진행
    date = sys.argv[3]
    print(f'<Crawling> {date} 일자 다음뉴스 크롤링을 시작합니다.')
    globals()[f'daumnews_{date}'] = get_daumnews_info(date)
    

    # 전처리 후 저장
    globals()[f'daumnews_{date}']['본문'] = globals()[f'daumnews_{date}']['본문'].apply(preprocess_content)
    globals()[f'daumnews_{date}'].to_csv(f'./다음뉴스_{date}_크롤링.csv', encoding='utf-8-sig', index=False)
    print(f'<Preprocessing> {date} 일자 다음뉴스 전처리 후 저장을 완료했습니다.')