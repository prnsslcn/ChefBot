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
    "title": "잘못된 질문",
    "ingredients": [],
    "steps": [
        "요리 관련 질문을 해주세요.",
        "음식과 관련된 주제를 입력하시면 더욱 적절한 레시피를 추천해 드릴 수 있습니다."
        ]   
    },
    {
    "title": "잘못된 질문",
    "ingredients": [],
    "steps": [
        "이 질문은 요리와 관련이 없습니다.",
        "음식 또는 조리법과 관련된 질문을 입력하시면 추천 레시피를 제공해 드릴 수 있습니다."
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
        "title": "잘못된 질문",
        "ingredients": [],
        "steps": [
            "요리에 대한 질문을 해주세요!",
            "예: '김치찌개 레시피 알려줘', '오늘 뭐 먹을까?'"
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
        "title": "수건 초콜릿",
        "ingredients": ["다크 초콜릿", "화이트 초콜릿", "코코아 가루", "연유", "버터"],
        "steps": [
            "1. 다크 초콜릿과 화이트 초콜릿을 중탕으로 녹입니다.",
            "2. 연유와 버터를 추가하여 부드러운 질감을 만듭니다.",
            "3. 초콜릿 반죽을 얇게 펴서 여러 겹으로 접어 수건 모양을 만듭니다.",
            "4. 코코아 가루를 뿌려 마무리한 후 냉장고에서 굳힙니다."
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
    },
    {
        "title": "된장찌개",
        "ingredients": ["된장", "두부", "애호박", "양파", "청양고추", "멸치 육수"],
        "steps": [
            "1. 냄비에 멸치 육수를 끓이고 된장을 풀어줍니다.",
            "2. 애호박, 양파, 청양고추를 넣고 끓입니다.",
            "3. 두부를 넣고 한소끔 더 끓이면 완성입니다."
        ]
    },
    {
        "title": "프렌치 토스트",
        "ingredients": ["식빵", "달걀", "우유", "설탕", "버터", "메이플 시럽"],
        "steps": [
            "1. 달걀과 우유, 설탕을 섞어 계란물을 만듭니다.",
            "2. 식빵을 계란물에 적신 후 팬에 버터를 두르고 굽습니다.",
            "3. 앞뒤로 노릇하게 구워 메이플 시럽을 뿌려 완성합니다."
        ]
    },
    {
        "title": "불고기",
        "ingredients": ["소고기", "간장", "설탕", "배즙", "마늘", "참기름", "양파"],
        "steps": [
            "1. 소고기를 얇게 썰어 간장, 설탕, 배즙, 마늘, 참기름에 재웁니다.",
            "2. 팬에 양파와 함께 볶아줍니다.",
            "3. 소고기가 익으면 완성입니다."
        ]
    },
     {
        "title": "치킨 마요 덮밥",
        "ingredients": ["밥", "닭가슴살", "마요네즈", "간장", "설탕", "쪽파", "김"],
        "steps": [
            "1. 닭가슴살을 삶은 후 잘게 찢어줍니다.",
            "2. 간장과 설탕을 넣고 닭가슴살을 간이 배도록 볶습니다.",
            "3. 밥 위에 볶은 닭가슴살을 올리고 마요네즈를 뿌려줍니다.",
            "4. 쪽파와 김가루를 올려 완성합니다."
        ]
    },
    {
        "title": "토마토 계란볶음",
        "ingredients": ["토마토", "달걀", "소금", "후추", "다진 마늘", "올리브오일"],
        "steps": [
            "1. 토마토를 먹기 좋은 크기로 썰어 준비합니다.",
            "2. 달걀을 풀어 스크램블 에그를 만들고 따로 둡니다.",
            "3. 팬에 다진 마늘을 볶은 후 토마토를 넣고 볶아줍니다.",
            "4. 스크램블 에그를 넣고 섞은 후 소금과 후추로 간을 맞춥니다."
        ]
    },
    {
        "title": "햄버거 스테이크",
        "ingredients": ["다진 소고기", "빵가루", "양파", "달걀", "소금", "후추", "스테이크 소스"],
        "steps": [
            "1. 다진 소고기에 잘게 썬 양파, 빵가루, 달걀을 넣고 반죽합니다.",
            "2. 반죽을 둥글고 평평한 모양으로 만들어 팬에 굽습니다.",
            "3. 양면이 노릇하게 익으면 스테이크 소스를 추가해 졸여줍니다.",
            "4. 접시에 담아 완성합니다."
        ]
    },
    {
        "title": "연어 스테이크",
        "ingredients": ["연어", "소금", "후추", "버터", "마늘", "레몬"],
        "steps": [
            "1. 연어에 소금과 후추로 밑간을 해둡니다.",
            "2. 팬에 버터를 녹인 후 마늘을 볶아 향을 냅니다.",
            "3. 연어를 팬에 올려 앞뒤로 노릇하게 구워줍니다.",
            "4. 접시에 담고 레몬을 곁들여 완성합니다."
        ]
    },
    {
        "title": "떡볶이",
        "ingredients": ["떡", "고추장", "고춧가루", "설탕", "어묵", "양파", "대파"],
        "steps": [
            "1. 냄비에 물을 넣고 고추장, 고춧가루, 설탕을 풀어 소스를 만듭니다.",
            "2. 떡과 어묵을 넣고 중불에서 끓여줍니다.",
            "3. 양파와 대파를 넣고 양념이 잘 배도록 졸여줍니다.",
            "4. 떡이 부드러워지면 완성입니다."
        ]
    },
    {
        "title": "감바스 알 아히요",
        "ingredients": ["새우", "마늘", "올리브오일", "페퍼론치노", "소금", "후추", "바게트"],
        "steps": [
            "1. 팬에 올리브오일을 넉넉히 두르고 마늘을 볶아줍니다.",
            "2. 페퍼론치노와 새우를 넣고 함께 볶아줍니다.",
            "3. 소금과 후추로 간을 맞춘 후 중약불에서 끓여줍니다.",
            "4. 바게트를 곁들여 완성합니다."
        ]
    },
    {
        "title": "팬케이크",
        "ingredients": ["밀가루", "베이킹파우더", "우유", "달걀", "설탕", "버터", "메이플 시럽"],
        "steps": [
            "1. 밀가루, 베이킹파우더, 설탕을 섞어 준비합니다.",
            "2. 우유와 달걀을 넣고 잘 섞어 반죽을 만듭니다.",
            "3. 팬에 버터를 두르고 반죽을 한 국자씩 부어 구워줍니다.",
            "4. 구운 팬케이크에 메이플 시럽을 뿌려 완성합니다."
        ]
    },
    {
        "title": "카레 라이스",
        "ingredients": ["카레 가루", "소고기", "감자", "당근", "양파", "밥"],
        "steps": [
            "1. 감자, 당근, 양파를 깍둑썰기하여 준비합니다.",
            "2. 냄비에 소고기를 볶은 후 감자, 당근, 양파를 추가합니다.",
            "3. 물을 붓고 끓인 후 카레 가루를 넣어 잘 섞습니다.",
            "4. 완성된 카레를 밥 위에 얹어 제공합니다."
        ]
    },
    {
        "title": "샌드위치",
        "ingredients": ["식빵", "슬라이스 햄", "치즈", "양상추", "토마토", "마요네즈"],
        "steps": [
            "1. 식빵 위에 마요네즈를 바릅니다.",
            "2. 슬라이스 햄, 치즈, 양상추, 토마토를 차례대로 올립니다.",
            "3. 다른 한 장의 식빵을 덮고 반으로 잘라 완성합니다."
        ]
    },
    {
        "title": "순두부찌개",
        "ingredients": ["순두부", "돼지고기", "양파", "청양고추", "고추장", "다진 마늘"],
        "steps": [
            "1. 냄비에 돼지고기를 볶다가 다진 마늘과 고추장을 추가합니다.",
            "2. 물을 넣고 끓이며 양파와 청양고추를 넣어줍니다.",
            "3. 순두부를 넣고 한소끔 더 끓여 완성합니다."
        ]
    }
]

samples_for_selector = [
    {
        "input": recipe["title"],  # 레시피 제목을 input으로 사용
        "output": f"재료: {', '.join(recipe['ingredients'])}\n과정: {' '.join(recipe['steps'])}"
    }
    for recipe in samples
]

print("samples_for_selector!!!!",samples_for_selector)

# 예제 선택기 (MMR 기반)
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples=samples_for_selector,
    embeddings=embedding_model,
    vectorstore_cls=FAISS,
    k=3
)



def parse_output(output_text):
    """
    'output'에서 '재료'와 '과정'을 추출하는 함수 (출력 키워드 없이도 동작하도록 수정)
    """
    # print("Parsing:", output_text)  #   디버깅용 출력 추가

    #  '재료:' 뒤의 내용과 '과정:' 뒤의 내용을 분리
    match = re.search(r"재료:\s*(.*?)\s*과정:\s*(.*)", output_text, re.DOTALL)
    
    if match:
        ingredients_text = match.group(1).strip()  # 재료 리스트 추출
        steps_text = match.group(2).strip()  # 조리 과정 추출

        #  ',' 기준으로 재료 분리
        ingredients = [i.strip() for i in ingredients_text.split(",")] if ingredients_text else []

        #  '1. ', '2. ' 같은 번호를 기준으로 과정 분리
        steps = [s.strip() for s in re.split(r"\d+\.\s*", steps_text) if s] if steps_text else []
    else:
        ingredients, steps = [], []

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

def generate_prompt(user_input):
    selected_examples = example_selector.select_examples({"input": user_input})
    example_text = "\n".join([    f"입력: {ex['input']}\n"    f"출력: {ex['output']}"    for ex in selected_examples])
    # print("example_text!!!!!",example_text)
   
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

    similar_recipes = search_similar_recipe(user_input, top_n=3)
    recipe_text = "\n\n".join([f"레시피 이름: {r['name']}\n재료: {r['ingredients']}" for r in similar_recipes])
    prompt = f"""
다음 사용자 입력과 유사한 레시피 데이터를 참고하여 요리를 추천해주세요.
아래 JSON 형식으로만 응답해주세요. 설명은 하지 마세요:
{{
  "title": "요리 이름",
  "ingredients": ["재료1", "재료2", "재료3"],
  "steps": ["1단계 설명", "2단계 설명", "3단계 설명"]
}}

참고 레시피:
{recipe_text}

예시:
{structured_examples}

사용자 입력: {user_input}
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
