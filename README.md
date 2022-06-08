# NLP-and-Information-Retrieval
CAU 2022-1 NLP and Information Retrieval Project Repository   
Check out Presentation at [Link]()

## 👪 Teammates
- Team name: **Tabloid Discriminator (찌라시 판별기)**
- **Seunguk Yu**: School of Computer Science & Engineering in CAU   
- **Minju Kim**: School of Computer Science & Engineering in CAU   
- **Hunseok Jeong**: School of Computer Science & Engineering in CAU

## 💡 Prototype
**Overall Flow**   
![Image](https://user-images.githubusercontent.com/80081345/172579215-a6de0302-f822-44da-82e1-4aa01eb45a8e.png)

## 🚂 Pipeline
### 1. Data Crawling & Preprocessing
Crawling some categories of Daum News by Selenium   
Preprocessing and Tokenization reflecting the characteristics of Korean by Konlpy
### 2. News Retrieval System
Implementing news retrieval for input query by Sklearn   
Removing similar news from retrieved results
### 3. News Evaluation 
Comparing retrieved results with Daum News by Selenium, Sklearn   
### 4. Service Visualization
Providing retrived news summary and visualization of service by NLTK, PyQt
