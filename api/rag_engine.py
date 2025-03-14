import numpy as np
import faiss
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
# 현재 FAISS 인덱스와 레시피 데이터를 활용하여 유사 레시피 검색 후 반환까지 테스트 진행

# OpenAI API 설정
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# 현재 스크립트(파일)가 있는 디렉토리를 기준으로 FAISS 인덱스 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 디렉토리

# 저장된 FAISS 인덱스 로드
index_path = os.path.join(BASE_DIR, "../vector_db/faiss_index/recipes_faiss.index")
index = faiss.read_index(index_path)
print(f" FAISS 인덱스 로드 완료, 저장된 벡터 개수: {index.ntotal}")

# 저장된 Json 파일 로드
json_path = os.path.join(BASE_DIR, "../data/recipes/")  
all_recipes = []
for filename in os.listdir(json_path):  
    if filename.endswith(".json"):  
        file_path = os.path.join(json_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            recipes = json.load(f)
            all_recipes.extend(recipes)  
print(f" 저장된 레시피 데이터 로드 완료, 저장된 레시피 개수: {len(all_recipes)}")

# 사용자 입력을 벡터화하는 함수
def get_embedding(user_input):
    response = client.embeddings.create(
        input=user_input, 
        model="text-embedding-ada-002"
    )
    return np.array(response.data[0].embedding).reshape(1, -1)  # FAISS 검색을 위해 2D 배열 변환

# 유사 레시피 검색 함수 (FAISS에서 바로 가져오기) (최종)
def search_similar_recipe(user_input, top_n=3):
    # 사용자 입력 임베딩
    user_embedding = get_embedding(user_input)
    # FAISS에서 유사한 레시피 검색 (L2 거리 기반)
    distances, indices = index.search(user_embedding, top_n)
    # 검색된 레시피 반환 (FAISS에서 직접 가져온 데이터 활용)
    similar_recipes = []
    for i in range(top_n):
        recipe_idx = indices[0][i]  # 검색된 레시피 인덱스
        similar_recipes.append(all_recipes[recipe_idx])  # 저장된 FAISS에서 직접 가져오기 
    return similar_recipes

# 테스트용 
if __name__ == "__main__":
    # 입력 받기
    user_input = input("재료나 메뉴를 입력하세요: ")
    # 유사 레시피 검색
    results = search_similar_recipe(user_input, top_n=3)

    print("\n 검색된 유사 레시피:")
    for idx, recipe in enumerate(results):
        print(f"\n{idx+1}. {recipe['name']}")
        print(f"   재료: {recipe['ingredients']}")
        print(f"   조리법: {recipe['recipe'][:2]}...")  # 조리법은 2단계까지만 출력
