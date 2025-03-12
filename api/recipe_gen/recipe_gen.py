## 모듈등록
import os
import langchain
import openai
from langchain_openai import OpenAI
import faiss

## api 키등록
# os - 파일경로 조작 , __file__ 현재 실행중인 Python 파일의 전체경로를 나타냄
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env") 
print(env_path)
def get_api_key(env_file):
    
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as file:  # UTF-8 인코딩 추가
            for line in file:
                line = line.strip()
                # print(f"{line}")  // 제대로 읽었는지 확인

                if line.startswith("OPENAI_API_KEY="):
                    key_value = line.split("=", 1)[1].strip().strip("'").strip('"')  # 작은따옴표 & 큰따옴표 제거
                    return key_value

    print("API KEY를 찾을 수 없음")  # 키를 찾지 못한 경우
    return None
# API 키 가져오기
API_KEY = get_api_key(env_path)
os.environ["OPENAI_API_KEY"] = API_KEY




