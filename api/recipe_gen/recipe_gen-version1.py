## 0. 모듈등록
import os
import langchain
import openai
from langchain_openai import OpenAI
import faiss

## 1. api 키등록

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

## 2. 모델 생성
os.environ["OPENAI_API_KEY"] = API_KEY

from langchain.chat_models import init_chat_model # 모델 생성

model = init_chat_model('gpt-4o-mini', model_provider='openai')

## 3. 텍스트 입력
# 텍스트 생성 기능 활용 -> 문장생성 혹은 질문과 답변등 추론능력 활용
res = model.invoke('닭가슴살 브로콜리 계란 으로 만들수 있는음식좀알려줄래?')

## 4. 출력
print(res)


