## 모듈등록
import os
import faiss
import langchain
import openai
from langchain_openai import OpenAI

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core import GPTVectorStoreIndex
# 라마인덱스, faiss 연동
from llama_index.core import StorageContext, GPTVectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.llms.openai import OpenAI

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


# 1. 데이터 로드
documents = SimpleDirectoryReader(input_dir="C:/Users/r2com/Documents/MiniProject3/data/recipes").load_data()
print(f"📂 {len(documents)}개의 문서를 로드했습니다.")

# 2. FAISS 벡터 DB 초기화 
embedding_dim = 1536  # OpenAI Embeddings 차원 수
faiss_index = faiss.IndexFlatL2(embedding_dim)

# 3. LLamaIndex에서 FAISS와 연동하여 벡터 DB 생성
vector_store = FaissVectorStore(faiss_index=faiss_index)  # FAISS를 벡터 저장소로 사용
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 4. LLamaIndex를 이용하여 문서를 벡터화하고 FAISS에 저장
index = GPTVectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)
print("✅ FAISS 벡터 DB 저장 완료!")

# 5. FAISS 인덱스 저장
save_dir = "C:/Users/r2com/Documents/MiniProject3/vector_db"
os.makedirs(save_dir, exist_ok=True)
faiss.write_index(faiss_index, os.path.join(save_dir, "recipes_faiss.index"))
print("✅ FAISS 인덱스 파일 저장 완료!")

# 6. GPT 모델 설정
llm = OpenAI(model="gpt-4o-mini")

# 7. LlamaIndex에서 OpenAI LLM을 사용하여 질의 응답 처리
query_engine = index.as_query_engine(llm=llm)

# 8. 사용자 질문 실행
query = "비밀의 방에 있는 물건은?"
response = query_engine.query(query)

print(f"🔍 질문: {query}")
print(f"🤖 GPT 응답: {response}")


