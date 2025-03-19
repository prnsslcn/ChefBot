import os
import json
import numpy as np
import faiss
import re
from flask import Flask, request, jsonify
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import numpy as np

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

# 잘못된 질문에대한 답변
invalid_samples = [
    {
    "title": "잘못된 질문",
    "ingredients": [],
    "steps": [
        "요리 관련 질문을 해주세요.",
        "음식과 관련된 주제를 입력하시면 더욱 적절한 레시피를 추천해 드릴 수 있습니다."
        ]   
    },
    {
    "title": "입력 필요",
    "ingredients": [],
    "steps": [
        "추천받고 싶은 요리나 식재료를 입력해주세요.",
        "예: '닭가슴살 요리 추천해줘', '브로콜리 활용한 음식 알려줘'"
        ]
    },
    {
        "title": "정보 부족",
        "ingredients": [],
        "steps": [
            "더 많은 정보를 입력해주세요.",
            "예: '고기 요리 추천', '아침 식사 메뉴 추천'"
        ]
    },
    {
        "title": "비요리 질문",
        "ingredients": [],
        "steps": [
            "요리와 관련된 질문을 해주세요.",
            "현재 시스템은 음식 추천 및 레시피 제공을 전문으로 합니다!"
        ]
    },
    {
        "title": "기술적인 질문",
        "ingredients": [],
        "steps": [
            "현재 음식 추천 서비스만 제공합니다.",
            "요리에 관한 질문을 입력해주세요!"
        ]
    },
        {
        "title": "잘못된 질문",
        "ingredients": [],
        "steps": [
            "요리 관련 질문을 해주세요.",
            "음식과 관련된 주제를 입력하시면 더욱 적절한 레시피를 추천해 드릴 수 있습니다."
        ]
    },
    {
        "title": "입력 필요",
        "ingredients": [],
        "steps": [
            "추천받고 싶은 요리나 식재료를 입력해주세요.",
            "예: '닭가슴살 요리 추천해줘', '브로콜리 활용한 음식 알려줘'"
        ]
    },
    {
        "title": "정보 부족",
        "ingredients": [],
        "steps": [
            "더 많은 정보를 입력해주세요.",
            "예: '고기 요리 추천', '아침 식사 메뉴 추천'"
        ]
    },
    {
        "title": "비요리 질문",
        "ingredients": [],
        "steps": [
            "요리와 관련된 질문을 해주세요.",
            "현재 시스템은 음식 추천 및 레시피 제공을 전문으로 합니다!"
        ]
    },
    {
        "title": "기술적인 질문",
        "ingredients": [],
        "steps": [
            "현재 음식 추천 서비스만 제공합니다.",
            "요리에 관한 질문을 입력해주세요!"
        ]
    },
    {
        "title": "로봇 만들어줘",
        "ingredients": [],
        "steps": [
            "현재 시스템은 요리 및 음식 추천을 전문으로 합니다.",
            "로봇 제작과 관련된 질문은 지원하지 않습니다."
        ]
    },
    {
        "title": "집 지어줘",
        "ingredients": [],
        "steps": [
            "현재 시스템은 건축과 관련된 정보를 제공하지 않습니다.",
            "요리 관련 질문을 입력해 주세요."
        ]
    },
    {
        "title": "날씨가 뭐야?",
        "ingredients": [],
        "steps": [
            "현재 시스템은 날씨 정보를 제공하지 않습니다.",
            "대신 요리에 관련된 질문을 해주시면 레시피를 추천해 드릴 수 있습니다!"
        ]
    },
    {
        "title": "운세 알려줘",
        "ingredients": [],
        "steps": [
            "운세 정보는 제공되지 않습니다.",
            "요리 관련 정보를 원하시면 질문을 입력해주세요!"
        ]
    },
    {
        "title": "수학 문제 풀어줘",
        "ingredients": [],
        "steps": [
            "현재 시스템은 수학 문제 해결을 지원하지 않습니다.",
            "대신 요리와 관련된 질문을 입력해 주세요."
        ]
    },
    {
        "title": "게임 추천해줘",
        "ingredients": [],
        "steps": [
            "현재 시스템은 게임 추천 기능을 제공하지 않습니다.",
            "대신 요리 및 음식 추천 서비스를 이용해 주세요."
        ]
    },
    {
        "title": "주식 전망 알려줘",
        "ingredients": [],
        "steps": [
            "현재 시스템은 금융 및 투자 정보를 제공하지 않습니다.",
            "요리 관련 질문을 입력해 주세요!"
        ]
    },
    {
        "title": "영화 추천해줘",
        "ingredients": [],
        "steps": [
            "현재 시스템은 영화 추천을 제공하지 않습니다.",
            "요리 관련 질문을 입력해 주세요!"
        ]
    },
    {
        "title": "AI가 세상을 정복할까?",
        "ingredients": [],
        "steps": [
            "흥미로운 질문이지만, 현재 시스템은 요리 추천 기능을 제공하고 있습니다.",
            "요리에 관한 질문을 입력해 주세요!"
        ]
    },
    {
        "title": "오늘의 뉴스 알려줘",
        "ingredients": [],
        "steps": [
            "현재 시스템은 뉴스 제공 기능을 지원하지 않습니다.",
            "요리에 대한 질문을 입력해 주세요!"
        ]
    }
]

# Few-Shot Learning 예제 (임의로 데이터 생성)
samples = [
     {
        "title": "두바이 초콜릿",
        "ingredients": ["카카오 열매", "설탕", "우유", "견과류", "향신료"],
        "steps": [
            "1. 카카오 열매를 발효 후 건조시킵니다.",
            "2. 원료를 정제하고 가공하여 초콜릿 베이스를 만듭니다.",
            "3. 다양한 견과류와 향신료를 추가해 두바이 스타일 초콜릿을 완성합니다.",
            "4. 화려한 금박을 입히거나 장식하여 고급스러운 느낌을 더합니다."
        ]
    },
    {
    "title": "요아정 (요거트 + 아이스크림)",
    "ingredients": ["그릭 요거트", "바나나", "블루베리", "꿀", "초콜릿 칩"],
    "steps": [
        "1. 그릭 요거트를 준비하여 볼에 담습니다.",
        "2. 바나나와 블루베리를 적당한 크기로 썰어 요거트 위에 올립니다.",
        "3. 꿀을 뿌린 후, 초콜릿 칩을 토핑으로 추가합니다.",
        "4. 냉동실에 30분 정도 살짝 얼려 시원한 디저트로 즐깁니다!"
        ]
    },
    {
        "title": "크로플 (크루아상 + 와플)",
        "ingredients": ["크루아상 생지", "버터", "설탕", "시럽", "과일 토핑"],
        "steps": [
            "1. 크루아상 생지를 와플 기계에 넣고 바삭하게 구워줍니다.",
            "2. 설탕과 버터를 녹여 크루아상 위에 뿌려줍니다.",
            "3. 시럽과 과일 토핑을 올려 완성합니다."
        ]
    },
    {
        "title": "김치볶음밥",
        "ingredients": ["밥", "김치", "대파", "달걀", "고추장", "참기름"],
        "steps": [
            "1. 대파를 송송 썰어 팬에 볶아 향을 내줍니다.",
            "2. 잘게 썬 김치를 넣고 볶다가 고추장을 추가합니다.",
            "3. 밥을 넣고 함께 볶아 간을 맞춥니다.",
            "4. 마지막으로 참기름을 두르고 달걀 프라이를 얹어 완성합니다."
        ]
    },
    {
        "title": "크림 파스타",
        "ingredients": ["스파게티 면", "생크림", "베이컨", "양파", "마늘", "파르메산 치즈"],
        "steps": [
            "1. 스파게티 면을 삶아 준비합니다.",
            "2. 팬에 마늘과 베이컨을 볶다가 양파를 추가합니다.",
            "3. 생크림을 넣고 졸인 후 삶은 면을 넣어 섞어줍니다.",
            "4. 마지막으로 파르메산 치즈를 뿌려 완성합니다."
        ]
    }
]

### 카테고리
# SBERT 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

# 카테고리별 음식 매핑
category_foods = {
    "한식": ["김치찌개", "비빔밥", "불고기", "된장찌개", "잡채"],
    "중식": ["짜장면", "짬뽕", "마파두부", "꿔바로우", "양장피"],
    "양식": ["파스타", "스테이크", "피자", "크림스프", "햄버거"],
    "일식": ["스시", "라멘", "돈카츠", "타코야끼", "오코노미야끼"]
}

# 카테고리 리스트
X_train = list(category_foods.keys())
# 카테고리 문장 임베딩 생성
X_train_vec = model.encode(X_train)
# 최근접 이웃 모델 학습 (카테고리 분류용)
knn = NearestNeighbors(n_neighbors=1, metric="cosine")
knn.fit(X_train_vec)

def recommend_foods(category_input):
    """
    입력된 카테고리에 해당하는 음식 5개 추천
    """
    #  category_input이 비어 있거나 None이면 빈 값 반환
    if not category_input or category_input.strip() == "":
        return None, []
    
    category_vec = model.encode([category_input])  # 입력값 임베딩
    _, indices = knn.kneighbors(category_vec)  # 가장 가까운 카테고리 찾기
    predicted_category = X_train[indices[0][0]]  # 예측된 카테고리

    # 디버깅용 출력
    print(f"🔹 입력값: {category_input}")
    print(f"🔹 예측된 카테고리: {predicted_category}")

    recommended_foods = category_foods.get(predicted_category, [])

    # 디버깅용 출력
    print(f"🔹 추천 음식 리스트: {recommended_foods}")

    return predicted_category, recommended_foods
###


# 잘못된 질문용 데이터 변환 (Few-Shot Learning을 위해 input-output 변환)
invalid_samples_for_selector = [
    {
        "input": sample["title"],
        "output": "\n".join(sample["steps"])  # Steps만 사용 (재료 없음)
    }
    for sample in invalid_samples
]
# MMR 기반 예제 선택기 (일반 요리 질문용)
samples_for_selector = [
    {
        "input": recipe["title"],  # 레시피 제목을 input으로 사용
        "output": f"재료: {', '.join(recipe['ingredients'])}\n과정: {' '.join(recipe['steps'])}"
    }
    for recipe in samples
]



# MMR 기반 예제 선택기 (잘못된 질문용)
invalid_example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples=invalid_samples_for_selector,
    embeddings=embedding_model,
    vectorstore_cls=FAISS,
    k=2
)
# 예제 선택기 (일반 음식용)
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples=samples_for_selector,
    embeddings=embedding_model,
    vectorstore_cls=FAISS,
    k=2
)

def parse_output(output_text):
    """
    'output'에서 '재료'와 '과정'을 추출하는 함수
    (빈 값이 있을 경우 원래 텍스트 유지)
    """
    print("Parsing:", output_text)  # 🔍 디버깅용 출력 추가

    #  '재료:' 뒤의 내용과 '과정:' 뒤의 내용을 분리
    match = re.search(r"재료:\s*(.*?)\s*과정:\s*(.*)", output_text, re.DOTALL)
    
    if match:
        ingredients_text = match.group(1).strip()  # 재료 리스트 추출
        steps_text = match.group(2).strip()  # 조리 과정 추출

        #  기준으로 재료 분리 (비어있을 경우 기존 텍스트 유지)
        ingredients = [i.strip() for i in ingredients_text.split(",")] if ingredients_text else [output_text]

        #  같은 번호를 유지하면서 과정 분리 (비어있을 경우 기존 텍스트 유지)
        step_list = re.findall(r"(\d+\.\s*.+)", steps_text)  # 숫자+점+공백 다음의 텍스트 추출
        steps = step_list if step_list else [output_text]
    else:
        #  '재료:'와 '과정:' 패턴이 없을 경우 원래 텍스트 그대로 사용
        ingredients, steps = [output_text], [output_text]

    return ingredients, steps


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

def generate_prompt(user_input,input_category):
    #카테고리
    predicted_category, recommended_foods = recommend_foods(input_category)

    selected_examples = example_selector.select_examples({"input": user_input})
    invalid_selected_examples = invalid_example_selector.select_examples({"input": user_input})

    #  '출력'에서 '재료'와 '과정'을 추출
    structured_examples = []
    for ex in selected_examples:
        ingredients, steps = parse_output(ex['output'])  #  수정된 함수 적용
        structured_examples.append({
            "title": ex["input"],  # 기존 input을 title로 사용
            "ingredients": ingredients,
            "steps": steps
        })
    print("structured_examples!!!!!",structured_examples)

     #  '출력'에서 '재료'와 '과정'을 추출
    invalid_structured_examples = []
    for ex in invalid_selected_examples:
        ingredients, steps = parse_output(ex['output'])  #  수정된 함수 적용
        invalid_structured_examples.append({
            "title": ex["input"],  # 기존 input을 title로 사용
            "ingredients": ingredients,
            "steps": steps
        })
    print("invalid_structured_examples!!!!!",invalid_structured_examples)

    similar_recipes = search_similar_recipe(user_input, top_n=3)
    recipe_text = "\n\n".join([f"레시피 이름: {r['name']}\n재료: {r['ingredients']}" for r in similar_recipes])
    
    # 카테고리 강제 지시 포함
    # prompt = f"""
    # 다음 사용자 입력에 따라 요리를 추천하되, 반드시 아래 **선택된 음식 카테고리**에 맞는 요리만 생성하세요.
    # 다른 카테고리의 음식이 나오면 안 됩니다.

    # [선택된 카테고리]: {input_category}
    # [카테고리 예시 음식]: {', '.join(recommended_foods)}

    # 반드시 아래 JSON 형식으로만 응답하세요 (불필요한 설명 문장 없이):
    # {{
    # "title": "요리 이름",
    # "ingredients": ["재료1", "재료2", "재료3"],
    # "steps": ["1단계 설명", "2단계 설명", "3단계 설명"]
    # }}

    # [유사한 기존 레시피 참고]:
    # {recipe_text}

    # [Few-shot 예시 레시피]:
    # {structured_examples}

    # [잘못된 질문 예시 응답 참고]:
    # {invalid_structured_examples}

    # [사용자 입력]:
    # {user_input}
    # """
    prompt = f"""
    다음 사용자 입력과 유사한 레시피 데이터를 참고하여 요리를 추천해주세요.
    **1번과 2번 규칙을 반드시 구분하고 JSON 형식으로만 응답해주세요.**  
    설명은 하지 마세요.

    **1번: 사용자 입력이 name 필드(요리명)과 일치하거나 유사하면**  
       - "요리이름 레시피" 형식으로 제공하세요.  
       - **요리의 재료(ingredients) 및 조리 과정(steps)도 포함하세요.**  
       - 이 경우 `"flag": "recipe"` 값을 응답에 포함하세요.

    **2번: 사용자 입력이 ingredients 필드(재료 목록)과 유사하면**  
       - "재료에 맞는 레시피를 추천해줄게요" 형식으로 제공하세요.  
       - **추천 레시피 3개만 반환**하고, **재료 및 요리 과정(ingredients & steps)은 제공하지 마세요.**  
       - 이 경우 이미지 생성 프롬프트를 생성하지 마세요
       - 이 경우 `"flag": "menu"` 값을 응답에 포함하세요.

    사용자 입력: {user_input}

    참고 레시피 데이터:
    {recipe_text}

    JSON 형식 예시(추천요리는 중복되지 않도록):
    {{
        "flag": "recipe" 또는 "menu",
        "title": "요리이름 레시피" 또는 "재료에 맞는 레시피를 추천해줄게요",
        "recommended_recipes": ["추천요리n"]
    }}
    """

    return prompt

def get_recipe_from_gpt(prompt):
    response = llm.invoke([{"role": "user", "content": prompt}])
    content = response.content.strip()
    json_start = content.find('{')
    json_end = content.rfind('}')
    try:
        if json_start != -1 and json_end != -1:
            json_str = content[json_start:json_end+1]
            return json.loads(json_str)
        else:
            raise ValueError("No valid JSON structure")
    except Exception:
        return {
            "title": "AI Generated Recipe",
            "ingredients": [],
            "steps": content.split('\n')
        }

# API 엔드포인트 생성
@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    user_input = data.get("user_input", "").strip()  # 문자열 공백 제거
    input_category = data.get("category", "").strip()  # 카테고리 추가

    if not user_input:
        return jsonify({"error": "user_input 파라미터가 필요합니다."}), 400

    # GPT 프롬프트 생성
    prompt = generate_prompt(user_input,input_category)
    print(f"\n[ 최종 프롬프트 확인]\n{prompt}")

    # GPT로부터 답변 생성 (Chat 모델 형식)
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    return jsonify({"user_input": user_input, "response": response.content})

# Flask 앱 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)