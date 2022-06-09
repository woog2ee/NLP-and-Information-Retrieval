import ast
import sys,os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from tokenizing import Tokenizer
tokenizer = Tokenizer()
vectorizer = TfidfVectorizer()



def get_tf_idf_query_similarity(docs_tfidf, query):
    # 쿼리 토큰화
    query_token = tokenizer.refine_text(query)
    query_token = tokenizer.get_clean_token(query_token)
   
    # 쿼리와 뉴스의 코사인 유사도 반환
    query_tfidf = vectorizer.transform([' '.join(query_token)])
    cos_sims = cosine_similarity(query_tfidf, docs_tfidf).flatten()
    return cos_sims
 
    
def retrieval(query, rank=5):
    # 쿼리 - 모든 뉴스의 (유사도,인덱스) 리스트 정렬
    print(f'\n[Tabloid Discriminator] "{query}" 검색을 준비합니다...')
    query = query.rstrip()
    cos_sims = get_tf_idf_query_similarity(docs_tfidf, query)
    cos_sims_item = sorted([(sim,i) for i,sim in enumerate(cos_sims)], reverse=True)
    
    # 상위 뉴스 리스트 반환
    ranked = []
    for sim,i in cos_sims_item[:rank*10]:
        ranked.append([df.iloc[i,1], df.iloc[i,2], i, sim])     # 뉴스 주소, 본문, 인덱스, 유사도
        
    # 검색된 뉴스 중, 내용 유사한 뉴스들 제거
    remove = []
    for i in range(rank*10):    
        if i in remove: continue
        idx = ranked[i][2]
        current_news = docs_tfidf[idx].toarray()
        
        for j in range(i+1, rank*10, 1):
            if j in remove: continue
            idx = ranked[j][2]
            next_news = docs_tfidf[idx].toarray()
            
            cos_sim = float(cosine_similarity(current_news, next_news))
            if cos_sim >= 0.95 and j not in remove:     
                remove.append(j)
                
    for i in range(len(remove)):
        idx = remove[len(remove)-1-i]
        ranked.pop(idx)
    ranked = ranked[:rank]

    # 상위 뉴스 유사도 출력
    for i in range(len(ranked)):
        sim = ranked[i][3]
        print(f'[Tabloid Discriminator] 쿼리-검색된 뉴스와의 유사도: {sim}')
    return ranked



# 다음 뉴스 읽어오기
input_file = './다음뉴스_202205_토큰화.csv'
df = pd.read_csv(input_file, header=0)

# 토큰 없는 뉴스들 제거
documents = []
remove = []	
for i,val in enumerate(df['본문토큰'].values):
    tokens = ast.literal_eval(val)
    if not tokens:
        remove.append(i)
        continue
    documents.append(' '.join(tokens))
df = df.drop(index=remove) 

# 뉴스 tf-idf 벡터화
docs_tfidf = vectorizer.fit_transform(documents)
