# ChefBot - 메뉴 기반 AI 레시피 추천  (Backend B)

## 📌 프로젝트 개요
이 브런치는 **FAISS 기반 AI 레시피 추천** 기능을 담당합니다.  
FAISS를 활용하여 **유사한 레시피를 빠르게 검색**하고, **GPT를 통해 보완된 추천을 제공**하는 것이 목표입니다.

---

## 📂 디렉토리 구조
```
    CHEFBOT/ 
    │ 
    ├── api/ 
    │   ├── image_gen.py 
    │   ├── rag_engine.py # FAISS 검색 기반 유사 레시피 추천 (유사 레시피 반환만 구현)
    │   ├── recipe_gen.py 
    │   ├── routes.py 
    │   ├── data/ # 데이터 저장소 
    │       ├── menu
    │       │   ├── *.txt,csv # 수집한 메뉴 데이터 
    │       ├── recipes
    │       │   ├── *.json # 스크래핑한 레시피 데이터(JSON) 
    │       ├── data_scraping_preprocessing.ipynb # 데이터 수집 및 전처리 코드 
    │   ├── scripts/  
    │   ├── vector_db/ # FAISS 벡터 데이터베이스 저장소 
    │       ├── faiss_index/ # FAISS 인덱스 파일 저장
    │       │     ├── recipes_faiss.index
    │       ├── vector_db_faiss.ipynb # FAISS 구축  
    ├── app.py # Flask 메인 애플리케이션 
    ├── README.md # 프로젝트 설명 파일 
    ├── requirements.txt # 필수 라이브러리 목록
```
---
## 📊 데이터 수집 & 전처리 과정

### 1️⃣ **메뉴 데이터 수집**
- **출처**: [서울관광재단_음식이미지정보]([https://www.seoultourism.kr](https://www.data.go.kr/data/15097008/fileData.do)/)  
- `MENU_NM`(메뉴 이름) 데이터를 추출  
- GPT에게 **최신 인기 메뉴** 요청하여 200개 추가 → **총 360개 메뉴 확보**  

### 2️⃣ **레시피 크롤링**
- **출처**: [만개의 레시피](https://www.10000recipe.com/)  
- 360개 메뉴명을 기준으로 **레시피 크롤링**  
- **재료, 조리법 데이터 전처리**하여 JSON 저장  

---

## ⚡ FAISS 구축 & 유사 레시피 추천

### 3️⃣ **FAISS 구축**
- 수집한 레시피 데이터를 **OpenAI Embedding 모델**을 이용해 벡터화  
- FAISS로 **빠른 유사도 검색이 가능하도록 인덱스 구축**  
- 벡터 데이터 저장 후, 검색 기능 구현  

### 4️⃣ **FAISS 기반 유사 레시피 추천 API**
- 사용자가 **재료 리스트를 입력하면**, FAISS에서 **가장 유사한 레시피 3개를 반환**  
- FAISS 인덱스를 통해 **유사 레시피 검색 속도 최적화**  


