import os
import json
import numpy as np
import faiss
from flask import Flask, request, jsonify
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector
from dotenv import load_dotenv

# Flask 앱 초기화
app = Flask(__name__)


# OpenAI API 키
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
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
    {
        "input": "두바이",
        "output": "두바이 초콜릿 만드는 방법\n1. 카카오 열매를 발효 후 건조시킵니다.\n2. 초콜릿 원료를 정제하고 가공하여 부드러운 질감을 만듭니다.\n3. 다양한 견과류와 향신료를 추가해 두바이 스타일 초콜릿을 완성합니다."
    },
    {
        "input": "피카소",
        "output": "피카소 스타일 푸드 아트 만드는 방법\n1. 다양한 색상의 소스를 준비합니다.\n2. 접시에 소스를 붓으로 칠하듯이 배치합니다.\n3. 미니멀한 재료 배치를 통해 예술적인 플레이팅을 완성합니다."
    },
    {
        "input": "우주 여행",
        "output": "우주 비행사들이 먹는 우주식품 만드는 방법\n1. 음식을 동결 건조하여 수분을 제거합니다.\n2. 진공 포장하여 가볍고 오래 보관할 수 있도록 합니다.\n3. 재수화 가능한 형태로 만들어 우주에서도 쉽게 조리할 수 있도록 합니다."
    },
    {
        "input": "올림픽",
        "output": "올림픽 선수들이 즐겨 먹는 고단백 식단\n1. 닭가슴살과 퀴노아를 기본으로 준비합니다.\n2. 다양한 채소와 견과류를 곁들여 균형 잡힌 영양을 제공합니다.\n3. 탄수화물과 단백질 비율을 조절하여 경기 전후 에너지를 보충합니다."
    },
    {
        "input": "AI 기술",
        "output": "AI가 추천하는 맞춤형 음식 레시피\n1. 개인의 식습관과 선호도를 분석합니다.\n2. AI가 영양 균형을 고려한 맞춤 레시피를 생성합니다.\n3. 재료 리스트와 조리법을 제공하여 최적의 요리를 완성합니다."
    },
    {
        "input": "해리포터",
        "output": "해리포터 속 버터맥주 만드는 방법\n1. 따뜻한 우유와 버터를 녹여 기본 베이스를 만듭니다.\n2. 바닐라 시럽과 카라멜을 추가하여 달콤한 맛을 더합니다.\n3. 크림을 얹어 마법사들이 즐기는 버터맥주를 완성합니다."
    },
    {
        "input": "NFT",
        "output": "NFT 테마 디저트 만들기\n1. 디지털 아트에서 영감을 얻은 색상의 마카롱을 준비합니다.\n2. 3D 프린팅 초콜릿을 활용해 독특한 장식을 추가합니다.\n3. 한정판 디저트로 만들어 NFT 컨셉을 반영합니다."
    },
    {
        "input": "여행 가방",
        "output": "여행 중 간편하게 먹을 수 있는 음식 준비법\n1. 견과류, 건과일, 에너지바를 개별 포장합니다.\n2. 진공 포장된 즉석 식사를 준비하여 쉽게 조리할 수 있도록 합니다.\n3. 수분 함량이 적고 보관이 쉬운 식품을 선택합니다."
    },
    {
        "input": "일론 머스크",
        "output": "일론 머스크가 추천하는 미래형 음식\n1. 대체 단백질 식품인 인공 고기 스테이크를 준비합니다.\n2. 식물성 우유와 곤충 단백질로 영양을 강화합니다.\n3. 지속 가능성과 미래 식량 문제 해결을 고려한 요리를 완성합니다."
    },
    {
        "input": "고흐의 별이 빛나는 밤",
        "output": "고흐의 별이 빛나는 밤을 닮은 디저트 만들기\n1. 블루베리와 레몬 커드를 활용한 파이를 준비합니다.\n2. 푸른색과 노란색의 아이싱을 이용해 밤하늘을 표현합니다.\n3. 초콜릿 별 장식을 더해 예술적인 디저트를 완성합니다."
    }
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
def search_similar_recipe(user_input, top_n=6):
    user_embedding = get_embedding(user_input)
    distances, indices = faiss_index.search(user_embedding, top_n)

    similar_recipes = []
    for i in range(top_n):
        recipe_idx = indices[0][i]
        if recipe_idx < len(all_recipes):  # 인덱스 범위 확인
            similar_recipes.append(all_recipes[recipe_idx])
    
    return similar_recipes

# GPT 프롬프트 생성
def generate_prompt(user_input):
    selected_examples = example_selector.select_examples({"input": user_input})
    example_text = "\n".join([f"입력: {ex['input']}\n출력: {ex['output']}" for ex in selected_examples])

    # 유사 레시피 검색 결과 추가
    similar_recipes = search_similar_recipe(user_input, top_n=3)
    recipe_text = "\n\n".join([f"레시피: {recipe['name']}\n재료: {', '.join(recipe['ingredients'])}" for recipe in similar_recipes])

    prompt = f"예제:\n{example_text}\n\n추천 레시피:\n{recipe_text}\n\n질문: {user_input}\n답변:"
    return prompt

# API 엔드포인트 생성
@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    user_input = data.get("user_input", "")

    if not user_input:
        return jsonify({"error": "user_input 파라미터가 필요합니다."}), 400

    # GPT 프롬프트 생성
    prompt = generate_prompt(user_input)
    #print(f"\n[ 최종 프롬프트 확인]\n{prompt}")

    # GPT로부터 답변 생성 (Chat 모델 형식)
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    return jsonify({"user_input": user_input, "response": response.content})

# Flask 앱 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
