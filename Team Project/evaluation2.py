from sklearn.feature_extraction.text import TfidfVectorizer
from tokenizing import Tokenizer
from retrieval import retrieval,get_tf_idf_query_similarity
from evaluation1 import Searcher
tokenizer = Tokenizer()
vectorizer = TfidfVectorizer()



def evaluate(query):
    # 뉴스 검색
    n = 5
    documents = []
    retrieval_news = retrieval(query, n)
    for i in range(len(retrieval_news)):
        content = retrieval_news[i][1]
        content_token = tokenizer.refine_text(content)
        content_token = tokenizer.get_clean_token(content_token)
        documents.append(' '.join(content_token))
    docs_tfidf = vectorizer.fit_transform(documents)

    # evaluation을 위한 크롤링 및 유사도 비교
    print('\n[Tabloid Discriminator] Evaluation을 위한 크롤링을 시작합니다...')
    searcher = Searcher(query, 10)
    answer = [False] * n
    for title,link,content in zip(searcher.searched_title, searcher.searched_link, searcher.searched_content):
        content_token = tokenizer.refine_text(content)
        content_token = tokenizer.get_clean_token(content)
        content_join = ' '.join(content_token)
        sim = get_tf_idf_query_similarity(vectorizer, docs_tfidf, content_join)

        for i in range(n):
            # 자체 검색 뉴스와, 다음 검색 뉴스의 유사도가 0.25 이상일 경우 참이라는 가정
            if sim[i] > 0.25: answer[i] = True

    # Mean Average Precision, MAP 계산
    avg = 0
    acc = 0
    for i in range(1, n+1):
        if answer[i-1]:
            acc += 1
            avg += acc / i
    print(f'> Evaluation을 통한 MAP: {avg/n}')
    return retrieval_news, zip(searcher.searched_title, searcher.searched_link, searcher.searched_content), avg/n