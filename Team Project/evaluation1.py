import re
import time
from selenium import webdriver



class Searcher:
    def __init__(self, query, n):
        # 뉴스사별 css selector 지정
        self.company_css_dict = {'동아일보': '#content > div > div.article_txt',
                                 '한국일보': 'body > div.wrap > div.container.end.end-uni > div.end-body > div > div.col-main.read',
                                 '서울경제': '#v-left-scroll-in > div.article_con > div.con_left > div.article_view',
                                 '연합뉴스': '#articleWrap > div.content01.scroll-article-zone01 > div > div > article',
                                 '서울신문': '#atic_txt1',
                                 '기독교연합신문': '#article-view-content-div',
                                 '주간동아': '#text',
                                 'YES24 채널예스': '#articleCont > div.viewType04 > div',
                                 'MBC': '#content > div > section.wrap_article > article > div.news_cont', 
                                 '뉴시스': '#content > div.articleView > div.view > div.viewer > article',
                                 '웹이코노미': '#container > div > div.column.sublay > div:nth-child(1) > div > div.arv_009 > div',
                                 '경인매일': '#article-view-content-div',
                                 '브레이크뉴스': '#contents_wrap_sub2 > div > div',
                                 '기호일보': '#article-view-content-div',
                                 '국제신문': '#news_textArea > div.news_article',
                                 '스포츠경향': '#articleBody',
                                 'KBS': '#harmonyContainer > section',
                                 '오마이뉴스': '#content_wrap > div.content > div.newswrap > div.news_body > div.news_view > div.article_view > div',
                                 '에이블뉴스': '#NewsContent',
                                 '세계일보': '#article_txt > article',
                                 '헤럴드경제': '#articleText',
                                 '경향신문': '#articleBody',
                                 '조선에듀': '#e_article > div.newsCnt',
                                 '여성신문': '#article-view-content-div',
                                 'ize': '#article-view-content-div',
                                 '한국경제': '#articletxt',
                                 'TV리포트': '#CmAdContent', 
                                 '스타뉴스': '#textBody',
                                 'SR타임스': '#articleBody',
                                 '머니투데이': '#textBody',
                                 '경북신문': '#contents > section:nth-child(3) > div > div.hm_col.hm_col2_21.col_left > div.view_body > div > div.view_article.clearfix',
                                 '중앙일보': '#article_body',
                                 '노컷뉴스': '#pnlContent',
                                 '프레시안': '#articleBody',
                                 '뉴스1': '#article_body_content'}
        # 크롤링 검색 결과
        searched_result       = self.get_searched_daumnews(query, n)
        self.searched_title   = searched_result[0]
        self.searched_link    = searched_result[1]
        self.searched_content = searched_result[2]
        
        
    def get_searched_daumnews(self, query, n):
        # 드라이버 실행
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument('--incognito')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        start_time = time.time()
        daumnews_link = f'https://search.daum.net/search?nil_suggest=btn&w=news&DA=STC&q={query}&period=u&sd=20220501000000&ed=20220531235959&p=1'
        driver = webdriver.Chrome('chromedriver.exe', options=options)     
        driver.implicitly_wait(3)
        driver.get(daumnews_link)

        # 검색된 뉴스 제목, 주소, 뉴스사, 본문
        searched_title   = []
        searched_link    = []
        searched_company = []
        searched_content = []

        # 검색 결과 뉴스 주소, 뉴스사 크롤링
        print('> 다음 뉴스 주소, 뉴스사 크롤링 시작합니다...\n')
        cnt = 0
        i = 1
        while (cnt < n) and (i <= 10):
            try:
                news    = driver.find_element_by_css_selector(f'#newsColl > div.cont_divider > ul > li:nth-child({i}) > div.wrap_cont > a')
                company = driver.find_element_by_css_selector(f'#newsColl > div.cont_divider > ul > li:nth-child({i}) > div.wrap_cont > span.cont_info > span:nth-child(1)')
                if company.text not in self.company_css_dict:
                    print(f'(뉴스사 "{company.text}" 정보 없음.)')
                    i += 1
                    continue  

                searched_title.append(news.text)
                searched_link.append(news.get_attribute('href'))
                searched_company.append(company.text)
                print(f'> {news.text} | {company.text}, 추가됨.')
                cnt += 1
                i += 1
            except Exception: 
                #print(Exception)
                i += 1
                continue

        # 검색 결과가 없을 경우
        print('> 크롤링 검색 결과가 없습니다.' if not searched_title else f'> crawling done: {len(searched_title)}')
        # 검색 결과 있을 경우 신문사 매핑
        searched_company = [self.company_css_dict[searched_company[i]] for i in range(len(searched_company))]

        # 뉴스별 본문 크롤링
        print('\n> 다음 뉴스 본문 크롤링 시작합니다...')
        remove = []
        for i in range(len(searched_link)):
            try:
                link = searched_link[i]
                driver.get(link)
                time.sleep(0.5)        

                cur_content = ''
                contents = driver.find_elements_by_css_selector(searched_company[i])
                for content in contents:
                    cur_content += content.text
                if not cur_content:
                    remove.append(i)     # 크롤링 안된 경우 인덱스 저장
                    continue
                cur_content = self.preprocess_content(cur_content)
                searched_content.append(cur_content)
            except:
                remove.append(i)

        # 크롤링 안된 뉴스 제거
        while remove:
            idx = remove.pop()
            searched_title.pop(idx)
            searched_link.pop(idx)
        searched_title = searched_title[:min(n, len(searched_title))]
        searched_link  = searched_title[:min(n, len(searched_link))]

        driver.quit()    
        print(f'\n> Evaluation을 위한 크롤링 수행 시간: {time.time()-start_time}')
        return searched_title, searched_link, searched_content


    def preprocess_content(self, text):    
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

        # 뉴스 추가 전처리
        stoptexts = ['관련기사', '영상취재', '저작권자', '답글 작성', '영문 번역에', '공유 기사저장', '좋아요 이미지', '유튜브로 보기', 'Copyright']
        for stoptext in stoptexts:
            text = re.sub(f'{stoptext}[\d\s\w.,!?]+', '', text)

        return text.strip()
