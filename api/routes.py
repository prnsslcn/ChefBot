from flask import Blueprint, jsonify, request
# from .recipe_gen import genarate_recipe # 임의 설정 함수명 통일해야함
from .image_gen import generate_image as generate_image_from_ai# 임의 설정 함수명 통일해야함
# from .rag_engine import search_similar_recipes # 임의 설정 함수명 통일해야함

routes = Blueprint('routes', __name__)

# 서버 테스트
@routes.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running"})

# GPT 레시피 생성
@routes.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    # data = request.get_json()
    # user_input = data.get("user_input", "")
    # recipe = genarate_recipe(user_input)
    # return jsonify({"recipe": recipe})
    return jsonify({"message": "generate_recipe"})

# 이미지 생성
@routes.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "")
    return generate_image_from_ai(prompt)
    # return jsonify({"message": generate_image})


# 통합 요청 API
# @routes.route("/query", methods=["POST"])
