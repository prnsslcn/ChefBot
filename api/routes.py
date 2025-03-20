import os
import json
import re
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from api.recipe_gen import generate_prompt  # 프롬프트 생성 함수 (RAG 포함)
from api.recipe_gen import final_prompt # 프롬프트 생성
from api.image_gen import generate_image as generate_image_ai
from langchain_openai import ChatOpenAI


# 환경 변수 로드 및 OpenAI API 설정
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)
llm = ChatOpenAI(model="gpt-4o-mini")

routes = Blueprint("routes", __name__)

# 서버 실행 테스트
@routes.route("/", methods=["GET"])
def home():
    print("[✔] 홈 엔드포인트 호출됨")
    return jsonify({"message": "Flask API is running"})

# 이미지 생성
@routes.route("/generate-image", methods=["POST"])
def generate_image():
    print("[📸] /generate-image 엔드포인트 호출됨")
    data = request.get_json()
    prompt = data.get("prompt", "")
    print(f"[📸] 생성 이미지 프롬프트: {prompt}")
    return generate_image_ai(prompt)

# 레시피 생성
@routes.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    print("[🍽️] /generate-recipe 엔드포인트 호출됨")
    data = request.get_json()
    user_input = data.get("user_input", "")
    input_category = data.get("category", "").strip() if data.get("category") else "기본 카테고리"

    print(f"[🍽️] 사용자 입력: {user_input}")

    if not user_input:
        return jsonify({"error": "user_input parameter is required."}), 400

    print("[🧠] 프롬프트 생성 중...")
    prompt = generate_prompt(user_input, input_category)  # ✅ 올바르게 수정!
    print(f"[🧠] 생성된 프롬프트:\n{prompt}")

    recipe = get_recipe_from_gpt(prompt)
    print("[✅] GPT로부터 레시피 생성 완료")

    return jsonify({"recipe": recipe})



# 통합 API
@routes.route("/query", methods=["POST"])
def handle_query():

    print("[🔗] /query 통합 API 호출됨")
    data = request.get_json()
    user_input = data.get("user_input", "").strip() 
    input_category = data.get("category", "").strip() 
    user_flag = data.get("flag", "").strip() 
    
    user_select = user_input
    flag = user_flag

    # 임의로 추가함
    # flag = 'detail'

    print(f"[🔗] 사용자 입력: {user_input}")
    print(f"[🔗] 카테고리: {input_category}")  # ✅ 로그 확인용

    if flag == 'select' :
        print("선택지 3개를 생성 하는중...")
        prompt = generate_prompt(user_input, input_category)

    
        top_3_recipes,matching_recipes = get_select_from_gpt(prompt) 
        print('top_3_recipes    ',top_3_recipes ,'matching_recipes',matching_recipes ) # 로그 확인용

        return top_3_recipes

    elif flag == 'detail' :
        print("선택한 메뉴를 생성하고 있습니다...",user_select)
        prompt = final_prompt(user_select)
        recipe = llm.invoke([{"role": "user", "content": prompt}])

        recipe = recipe.content.strip()
        recipe = clean_json_response(recipe)
        # print("[🤖] GPT 응답 내용:\n", recipe)
        recipe = json.loads(recipe)  # JSON 문자열 → Python 딕셔너리 변환
        print("recipe!!!!!!!!!!!!!!!@@@@@",recipe)
        print("[✅] 레시피 생성 완료")

        # ✅ 개선된 이미지 프롬프트 구성 (title + ingredients 활용)
        title = recipe.get("title", "요리")
        ingredients = recipe.get("ingredients", [])
        ingredient_text = ", ".join(ingredients)

        image_prompt = f"A photo of a dish called '{title}' made with {ingredient_text}."
        print(f"[🎨] 이미지 생성 프롬프트: {image_prompt}")

        image_response = generate_image_ai(image_prompt).get_json()
        image_url = image_response.get("image_url", "")
        print(f"[✅] 이미지 URL 생성 완료: {image_url}")

        return jsonify({
            "recipe": recipe,
            "image_url": image_url
        })

    else:
        return jsonify({"error": "Invalid flag value."}), 400

    if not user_input:
        return jsonify({"error": "user_input parameter is required."}), 400

    try:
        print("[🔍] RAG 기반 프롬프트 생성 시작...")
        prompt = generate_prompt(user_input, input_category)
        print(f"[📤] 생성된 프롬프트:\n{prompt}")

        print("[🍳] GPT 레시피 생성 중...")
        recipe = get_recipe_from_gpt(prompt)
        print("recipe!!!!!!!!!!!!!!!@@@@@",recipe)
        print("[✅] 레시피 생성 완료")

        # ✅ 개선된 이미지 프롬프트 구성 (title + ingredients 활용)
        title = recipe.get("title", "요리")
        ingredients = recipe.get("ingredients", [])
        ingredient_text = ", ".join(ingredients)

        image_prompt = f"A photo of a dish called '{title}' made with {ingredient_text}."
        print(f"[🎨] 이미지 생성 프롬프트: {image_prompt}")

        image_response = generate_image_ai(image_prompt).get_json()
        image_url = image_response.get("image_url", "")
        print(f"[✅] 이미지 URL 생성 완료: {image_url}")

        return jsonify({
            "recipe": recipe,
            "image_url": image_url
        })

    except Exception as e:
        print(f"[❌] 에러 발생: {str(e)}")
        return jsonify({"error": str(e)}), 500

##################
def clean_json_response(response_content):
    """
    GPT 응답에서 Markdown 코드 블록 (` ```json ... ``` `)을 제거하는 함수
    """
    # ✅ "```json" 및 "```" 제거
    response_content = response_content.replace("```json", "").replace("```", "").strip()
    return response_content
##################
def convert_list_to_dict(recipe_list):
    """
    GPT 응답이 리스트([]) 형태일 경우, 첫 번째 레시피만 반환하는 딕셔너리({})로 변환
    """
    if not recipe_list:
        return {
            "title": "AI Generated Recipe",
            "ingredients": [],
            "steps": []
        }

    if isinstance(recipe_list, list):
        # ✅ 첫 번째 레시피만 반환
        return recipe_list[0]

    return recipe_list  # 이미 딕셔너리({})면 그대로 반환
##################
def convert_list_to_dicts(recipe_list):
    """
    GPT 응답이 리스트([]) 형태일 경우, 모든 레시피를 변환하여 반환하는 함수
    """
    if not recipe_list:
        return [{
            "title": "AI Generated Recipe",
            "ingredients": [],
            "steps": []
        }]

    if isinstance(recipe_list, list):
        # ✅ 모든 레시피 반환
        return recipe_list  

    return [recipe_list]  # 이미 딕셔너리({})면 리스트에 담아서 반환

##################
def extract_user_input(prompt):
    """
    prompt에서 [사용자 입력]: 이후의 값을 추출하는 함수
    """
    match = re.search(r"\[사용자 입력\]:\s*(.+)", prompt)
    if match:
        return match.group(1).strip()
    return None  # 사용자 입력이 없을 경우 None 반환
##################
from sentence_transformers import SentenceTransformer
import numpy as np
# ✅ SBERT 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_top_similar_recipes(user_input, recipe_titles, top_n=3):
    """
    user_input과 recipe_titles 간의 유사도를 비교하여
    가장 유사한 top_n개의 레시피를 반환하는 함수
    """
    # 1️⃣ user_input과 recipe_titles를 벡터화
    user_input_vec = model.encode([user_input])  # (1, dim)
    recipe_vecs = model.encode(recipe_titles)  # (N, dim)

    # 2️⃣ 코사인 유사도 계산
    similarities = np.dot(recipe_vecs, user_input_vec.T).flatten()

    # 3️⃣ 가장 유사한 top_n개의 인덱스 찾기
    top_indices = np.argsort(similarities)[::-1][:top_n]

    # 4️⃣ 유사한 레시피 반환
    top_recipes = [recipe_titles[i] for i in top_indices]

    return top_recipes
##################
def filter_top_recipes(recipe_data, top_3_recipes):
    """
    recipe_data 리스트에서 top_3_recipes의 title과 일치하는 레시피를 반환하는 함수
    """
    filtered_recipes = [recipe for recipe in recipe_data if recipe["title"] in top_3_recipes]
    return filtered_recipes
##################
# GPT 응답을 JSON으로 파싱
def get_recipe_from_gpt(prompt):
    print("[🤖] get_recipe_from_gpt() 호출됨",prompt)
    response = llm.invoke([{"role": "user", "content": prompt}])
    content = response.content.strip()
    content=clean_json_response(content)
    print("[🤖] GPT 응답 내용:\n", content)

    ####################
    user_input=extract_user_input(prompt)

    # JSON 파싱 시도
    recipe_data = json.loads(content)
    # title만 리스트로 저장
    recipe_titles = [recipe["title"] for recipe in recipe_data]
    print("[📌] 추출된 레시피 제목 리스트:", recipe_titles)

    top_3_recipes = get_top_similar_recipes(user_input, recipe_titles)
    print("🥇 가장 유사한 3가지 메뉴:", top_3_recipes)

    matching_recipes = filter_top_recipes(recipe_data,top_3_recipes)

    # print("matching_recipes!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",matching_recipes)
    test=convert_list_to_dicts(matching_recipes)
    print('test!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',test)
          
    ####################

    try:
        # ✅ JSON 파싱 시도
        recipe_data = json.loads(content)
        print("[🤖] recipe_data 응답 내용:\n", recipe_data)

        print("[🤖] convert_list_to_dict(recipe_data) 응답 내용:\n", convert_list_to_dict(recipe_data))

        # ✅ 리스트([]) → 딕셔너리({}) 변환
        return convert_list_to_dict(recipe_data)
        

    except json.JSONDecodeError:
        print("[⚠️] JSON 파싱 실패. fallback 처리됨.")
        return {
            "title": "AI Generated Recipe",
            "ingredients": [],
            "steps": content.split('\n')  # 응답을 줄 단위로 분리
        }
##############################################
import json

def convert_top_3_to_json(top_3_recipes):
    """
    🛠️ top_3_recipes 리스트를 JSON 형태로 변환하는 함수
    """
    if not top_3_recipes or not isinstance(top_3_recipes, list):
        return json.dumps({"error": "No recipes found."}, ensure_ascii=False)
    
    # 🔹 JSON 형태로 변환
    json_data = {"recipes": [ recipe for recipe in top_3_recipes]}
    
    return json.dumps(json_data, ensure_ascii=False)  # ✅ 한글 깨짐 방지
##############################################
# 선택지 반환 함수
def get_select_from_gpt(prompt):
    print("[🤖] get_recipe_from_gpt() 호출됨",prompt)
    response = llm.invoke([{"role": "user", "content": prompt}])
    content = response.content.strip()
    content=clean_json_response(content)
    print("[🤖] GPT 응답 내용:\n", content)

    ####################
    user_input=extract_user_input(prompt)

    # JSON 파싱 시도
    recipe_data = json.loads(content)
    # title만 리스트로 저장
    recipe_titles = [recipe["title"] for recipe in recipe_data]
    print("[📌] 추출된 레시피 제목 리스트:", recipe_titles)

    top_3_recipes = get_top_similar_recipes(user_input, recipe_titles)
    print("🥇 가장 유사한 3가지 메뉴:", top_3_recipes)

     # 🔹 JSON 변환 함수 호출
    top_3_recipes = convert_top_3_to_json(top_3_recipes)

    matching_recipes = filter_top_recipes(recipe_data,top_3_recipes)
    
    # print("matching_recipes!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",matching_recipes)
    matching_recipes=convert_list_to_dicts(matching_recipes)
    print('test!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',matching_recipes)

    return top_3_recipes,matching_recipes
##############################################

