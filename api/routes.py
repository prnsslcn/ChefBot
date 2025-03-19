import os
import json
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from api.recipe_gen import generate_prompt  # 프롬프트 생성 함수 (RAG 포함)
from api.recipe_gen import generate_recommendation  # 추천 메뉴 생성 함수
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
    print(f"[🍽️] 사용자 입력: {user_input}")

    if not user_input:
        return jsonify({"error": "user_input parameter is required."}), 400

    print("[🧠] 프롬프트 생성 중...")
    prompt = generate_prompt(user_input)
    print(f"[🧠] 생성된 프롬프트:\n{prompt}")

    recipe = get_recipe_from_gpt(prompt)
    print("[✅] GPT로부터 레시피 생성 완료")

    return jsonify({"recipe": recipe})

# 메뉴 추천 API
@routes.route("/recommend-menu", methods=["POST"])
def recommend_menu():
    print("[🍲] /recommend-menu 엔드포인트 호출됨")
    data = request.get_json()
    user_input = data.get("user_input", "")
    print(f"[🍲] 사용자 입력: {user_input}")

    if not user_input:
        return jsonify({"error": "user_input parameter is required."}), 400

    print("[🧠] 프롬프트 생성 중...")
    prompt = generate_recommendation(user_input)
    print(f"[🧠] 생성된 프롬프트:\n{prompt}")

    # GPT 호출 
    response = llm.invoke([{"role": "user", "content": prompt}])
    gpt_output = response.content.strip()
    
    print(f"[🤖] GPT 응답 내용:\n{gpt_output}")

    try:
        menu_list = json.loads(gpt_output)  
        menu_names = [item.get("title", "요리 이름") for item in menu_list]

    except json.JSONDecodeError:
        print("[❌] JSON 변환 실패: GPT 응답이 올바르지 않음")
        return jsonify({"error": "Invalid response format from GPT"}), 500

    print(f"[✅] 추천 메뉴 목록: {menu_names}")

    return jsonify({"menu_names": menu_names})

# 통합 API
@routes.route("/query", methods=["POST"])
def handle_query():
    print("[🔗] /query 통합 API 호출됨")
    data = request.get_json()
    user_input = data.get("user_input", "")
    # input_category = data.get("category", "").strip() # 주석 처리 해놓았음
    input_category = ""
    
    print(f"[🔗] 사용자 입력: {user_input}")
    print(f"[🔗] 카테고리: {input_category}")

    if not user_input:
        return jsonify({"error": "user_input parameter is required."}), 400

    try:
        print("[🔍] RAG 기반 프롬프트 생성 시작...")
        prompt = generate_prompt(user_input, input_category)
        print(f"[📤] 생성된 프롬프트:\n{prompt}")

        print("[🍳] GPT 레시피 생성 중...")
        recipe = get_recipe_from_gpt(prompt)
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


# GPT 응답을 JSON으로 파싱
def get_recipe_from_gpt(prompt):
    print("[🤖] get_recipe_from_gpt() 호출됨")
    response = llm.invoke([{"role": "user", "content": prompt}])
    content = response.content.strip()
    print("[🤖] GPT 응답 내용:\n", content)

    json_start = content.find("{")
    json_end = content.rfind("}")
    try:
        if json_start != -1 and json_end != -1:
            json_content = content[json_start:json_end+1]
            recipe = json.loads(json_content)
            return recipe
        else:
            raise ValueError("No valid JSON found.")
    except Exception:
        print("[⚠️] JSON 파싱 실패. fallback 처리됨.")
        return {
            "title": "AI Generated Recipe",
            "ingredients": [],
            "steps": content.split('\\n')
        }
