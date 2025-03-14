import os
import faiss
from flask import Flask, request, jsonify
from langchain_openai import OpenAI
from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from llama_index.core import GPTVectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.vector_stores.faiss import FaissVectorStore
from langchain_openai import ChatOpenAI  # ✅ OpenAI 대신 ChatOpenAI 사용

# ✅ Flask 앱 초기화
app = Flask(__name__)

# ✅ OpenAI API 키 설정
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

# ✅ GPT 모델 설정
llm = OpenAI(model="gpt-4o-mini")
# ✅ GPT 모델 설정
llm = ChatOpenAI(model="gpt-4o-mini")

# ✅ FAISS 벡터 DB 설정
embedding_dim = 1536
faiss_index = faiss.IndexFlatL2(embedding_dim)
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# ✅ 데이터 로드 및 벡터화
documents = SimpleDirectoryReader(input_dir="C:/Users/r2com/Documents/MiniProject3/data/recipes").load_data()
index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)

# ✅ Few-Shot Learning 예제
samples = [
    {"input": "자동차의 엔진 작동 원리는?", "output": "1. 엔진은 연료를 연소시켜 에너지를 생성합니다. ..."},
    {"input": "코딩을 배우는 단계는?", "output": "1. 프로그래밍 언어의 문법을 익힙니다. ..."},
    {"input": "커피가 만들어지는 과정은?", "output": "1. 커피 원두를 수확하고 건조시킵니다. ..."}
]

example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples=samples,
    embeddings=OpenAIEmbeddings(),
    vectorstore_cls=FAISS,
    k=3
)

# ✅ MMR 기반 문서 검색 (FAISS)
def retrieve_relevant_docs(query):
    retriever = index.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    retriever_docs = retriever.retrieve(query)
    return "\n".join([doc.text for doc in retriever_docs])

# ✅ GPT 프롬프트 생성
def generate_prompt(query):
    selected_examples = example_selector.select_examples({"input": query})
    example_text = "\n".join([f"입력: {ex['input']}\n출력: {ex['output']}" for ex in selected_examples])
    context = retrieve_relevant_docs(query)
    prompt = f"예제:\n{example_text}\n\n문맥:\n{context}\n\n질문: {query}\n답변:"
    return prompt

# ✅ API 엔드포인트 생성
@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "query 파라미터가 필요합니다."}), 400

    # ✅ GPT 프롬프트 생성
    prompt = generate_prompt(query)
    print(f"\n[📌 최종 프롬프트 확인]\n{prompt}")

    # ✅ GPT로부터 답변 생성 (Chat 모델 형식)
    response = llm.invoke([{"role": "user", "content": prompt}])
    
    return jsonify({"query": query, "response": response.content})  # .content 추가

# ✅ Flask 앱 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
