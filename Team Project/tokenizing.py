import pandas as pd
from tqdm import tqdm
from konlpy.tag import Okt



class Tokenizer:
    def __init__(self):
        self.okt = Okt()
        self.stopwords = []
        stopwords_path = './stopwords-ko.txt'
        with open(stopwords_path, 'r', encoding='UTF-8') as file:
            for line in file:
                self.stopwords.append(line.strip())
                
                
    # 특수문자 및 불용어 제거, 공백 간격 토큰화
    def refine_text(self, text):
        # 특수문자 제거
        special_characters = ['!', '?', '"','#','$','%','&','(',')','*','+',
                              '/',':',';','<','=','>','@','[','\\',']','^',
                              '`','{','|','}','~','\t', '\n', '-', ',', '.']
        for i in range(len(text)):
            for ch in special_characters:
                text = text.replace(ch, '')
        text = text.strip()
        
        # 공백 간격 토큰화, 불용어 제거
        word_list = text.split()
        for word in word_list:
            if word in self.stopwords:
                while word in word_list: word_list.remove(word)
                    
        # 리스트 중복 제거
        word_list = list(set(word_list))
        return word_list
    
    
    # 형태소 분석 및 어간 추출
    def get_clean_token(self, word_list):
        clean_word_list = []
        for word in word_list:
            #print(word)
            # 품사 정보 획득
            word_info = self.okt.pos(word)
            if len(word_info) == 0: continue
            
            # 불필요한 품사 분리
            drop_idx = []
            for i in range(len(word_info)):    
                if word_info[i][1] in ['Suffix', 'Number', 'Determiner', 'Alpha']:
                    word_info = []
                    break
                if word_info[i][1] in ['Josa', 'Foreign']:
                    drop_idx.append(i)
            
            try:
                for i in range(len(drop_idx)):
                    idx = drop_idx[len(drop_idx)-1-i]
                    word_info.pop(idx)
            except: continue     # 단어 자체를 사용하지 않을 경우 넘김

            # 필요한 형태소 원형 복구
            if len(word_info) == 0: continue
            else: 
                clean_word = ''
                for i in range(len(word_info)):
                    clean_word += word_info[i][0]

                morph_info = self.okt.morphs(clean_word, stem=True)
                morph_word = ''
                for i in range(len(morph_info)):
                    morph_word += morph_info[i]
                clean_word = morph_word
                
                # 표현 정제
                if len(clean_word) == 1: continue
                if len(clean_word) > 2 and clean_word[-1] in ['되', '돼', '하', '해']:
                    clean_word = clean_word[:len(clean_word)-1]
                clean_word_list.append(clean_word)
                
        # 리스트 중복 제거
        clean_word_list = list(set(clean_word_list))
        return clean_word_list



if __name__ == "__main__":
    # 다음 뉴스 읽어오기
    data = pd.read_csv('')
    data = data.dropna(subset=['본문'])
    tqdm.pandas()
    
    
    # 본문 토큰화
    tokenizer = Tokenizer()
    data['제목토큰'] = data['제목']
    data['제목토큰'] = data['제목토큰'].progress_apply(tokenizer.refine_text)
    data['제목토큰'] = data['제목토큰'].progress_apply(tokenizer.get_clean_token)
    
    data['본문토큰'] = data['본문']
    data['본문토큰'] = data['본문토큰'].progress_apply(tokenizer.refine_text)
    data['본문토큰'] = data['본문토큰'].progress_apply(tokenizer.get_clean_token)
    
    
    # 토큰화 후 저장
    data.to_csv('', encoding='utf-8-sig', index=False)