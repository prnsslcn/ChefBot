import os
import json
import numpy as np
import faiss
from flask import Flask, request, jsonify
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector

# Flask 앱 초기화
app = Flask(__name__)

# OpenAI API 키 설정
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

def get_api_key(env_file):
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line.startswith("OPENAI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("'").strip('"')
    print("API KEY를 찾을 수 없음")
    return None

API_KEY = get_api_key(env_path)
os.environ["OPENAI_API_KEY"] = API_KEY
client = OpenAI(api_key=API_KEY)

# GPT 모델 설정
llm = ChatOpenAI(model="gpt-4o-mini")
embedding_model = OpenAIEmbeddings()

# 현재 파일 기준 상대 경로로 FAISS 인덱스 및 레시피 데이터 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(BASE_DIR, "../vector_db/faiss_index/recipes_faiss.index")
json_dir = os.path.join(BASE_DIR, "../data/recipes/")

# FAISS 인덱스 불러오기
if not os.path.exists(index_path):
    raise FileNotFoundError(f"FAISS 인덱스 파일을 찾을 수 없습니다: {index_path}")

faiss_index = faiss.read_index(index_path)
#print(f" FAISS 인덱스 로드 완료! 저장된 벡터 개수: {faiss_index.ntotal}")

# 저장된 JSON 파일에서 레시피 데이터 로드
all_recipes = []
for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(json_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            recipes = json.load(f)
            all_recipes.extend(recipes)

#print(f" 저장된 레시피 데이터 로드 완료! 총 {len(all_recipes)}개 레시피")

# Few-Shot Learning 예제
samples = [
    {"input": "김치찌개 만드는 법", "output": "1. 김치를 볶고 돼지고기를 추가합니다. ..."},
    {"input": "떡볶이 재료", "output": "1. 떡, 고추장, 설탕, 간장, 물을 준비합니다. ..."},
    {"input": "파스타를 맛있게 만드는 방법", "output": "1. 파스타 면을 삶고, 소스를 곁들입니다. ..."}
]

# Few-Shot Learning을 위한 FAISS 메모리 벡터 저장소 생성
sample_texts = [s["input"] for s in samples]
sample_outputs = [s["output"] for s in samples]

sample_vector_store = FAISS.from_texts(
    sample_texts, 
    embedding_model
)

# 예제 선택기 (MMR 기반)
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples=samples,
    embeddings=embedding_model,
    vectorstore_cls=FAISS,
    k=3
)

# 사용자 입력을 벡터화하는 함수
def get_embedding(user_input):
    response = client.embeddings.create(
        input=user_input,
        model="text-embedding-ada-002"
    )
    return np.array(response.data[0].embedding).reshape(1, -1)  # FAISS 검색을 위해 2D 배열 변환

# 유사 레시피 검색 함수
def search_similar_recipe(user_input, top_n=3):
    user_embedding = get_embedding(user_input)
    distances, indices = faiss_index.search(user_embedding, top_n)

    similar_recipes = []
    for i in range(top_n):
        recipe_idx = indices[0][i]
        if recipe_idx < len(all_recipes):  # 인덱스 범위 확인
            similar_recipes.append(all_recipes[recipe_idx])
    
    return similar_recipes

# GPT 프롬프트 생성
def generate_prompt(query):
    selected_examples = example_selector.select_examples({"input": query})
    example_text = "\n".join([f"입력: {ex['input']}\n출력: {ex['output']}" for ex in selected_examples])

    # 유사 레시피 검색 결과 추가
    similar_recipes = search_similar_recipe(query, top_n=3)
    recipe_text = "\n\n".join([f"레시피: {recipe['name']}\n재료: {', '.join(recipe['ingredients'])}" for recipe in similar_recipes])

    prompt = f"예제:\n{example_text}\n\n추천 레시피:\n{recipe_text}\n\n질문: {query}\n답변:"
    return prompt

# API 엔드포인트 생성
@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "query 파라미터가 필요합니다."}), 400

    # GPT 프롬프트 생성
    prompt = generate_prompt(query)
    #print(f"\n[ 최종 프롬프트 확인]\n{prompt}")

    # GPT로부터 답변 생성 (Chat 모델 형식)
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    return jsonify({"query": query, "response": response.content})

# Flask 앱 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
