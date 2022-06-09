import numpy as np
import networkx as nx
from nltk.cluster.util import cosine_distance
from tokenizing import Tokenizer



# 정의한 tokenizer로 토큰화
def get_token(text):
    tokenizer = Tokenizer()
    token = tokenizer.refine_text(text)
    token = tokenizer.get_clean_token(token)
    return token


# 텍스트 읽고 분리
def read_article(filedata):
    filedata = filedata.replace('?','.')
    article = filedata.split('. ')
    sentences = []
    for sentence in article:
        token = get_token(sentence)
        if len(token) > 0:
            sentences.append([sentence, get_token(sentence)])
    return sentences


# 문장 코사인 유사도 반환
def sentence_similarity(sent1, sent2):
    # 벡터 틀 생성
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # 각 문장 벡터 생성
    for w in sent1:
        vector1[all_words.index(w)] += 1
    for w in sent2:
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)
 

# 문장 코사인 유사도 행렬 반환 
def build_similarity_matrix(sentences):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2])
    return similarity_matrix


# 텍스트 요약
def generate_summary(file_name, top_n=5):
    # 텍스트 읽고 분리
    sentences = read_article(file_name)

    # 문장 코사인 유사도 행렬 생성
    sentence_similarity_martix = build_similarity_matrix([i[1] for i in sentences])

    # 문장 코사인 유사도 행렬 정렬
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # 상위 문장 선택을 통한 요약
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    summarized_text = []
    if len(ranked_sentence) <= top_n:
        top_n = len(ranked_sentence)
    for i in range(top_n):
      summarized_text.append(ranked_sentence[i][1][0])
    return '. '.join(summarized_text)