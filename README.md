# Atelier
CAU 2022-1 NLP and Information Retrieval Project Repository   
Check out Presentation at [Link](https://github.com/woog2ee/NLP-and-Information-Retrieval/blob/main/Team%20Project/Tabloid%20Discriminator%20Presentation.pdf)

## 👪 Teammates
- Team name: **Kakaotalk Tabloid Discriminator (카카오톡 찌라시 판별기)**
- **Seunguk Yu**: School of Computer Science & Engineering in CAU   
- **Minju Kim**: School of Computer Science & Engineering in CAU   
- **Hunseok Jeong**: School of Computer Science & Engineering in CAU

## 💡 Prototype
**Overall Flow**   
![Image](https://user-images.githubusercontent.com/80081345/173246811-ad11a830-c05f-45ec-8d3d-e137466467e8.png)

**News Search with Summarization**   
![Image](https://user-images.githubusercontent.com/80081345/173246843-9fc1b23c-c763-4e0c-a04a-7916b0c63641.png)

**News Search with Evaluation**   
![Image](https://user-images.githubusercontent.com/80081345/173246882-eb42444d-2f13-43f3-9e2e-f428ae4cf8f8.png)

**Terminal Status**   
![Image](https://user-images.githubusercontent.com/80081345/173246896-1ebeea8c-e1cc-4336-88a3-4137e3874a25.png)

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
