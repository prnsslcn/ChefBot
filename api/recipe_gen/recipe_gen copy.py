## 모듈등록
import os
import faiss
import langchain
import openai
from langchain_openai import OpenAI
from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector
# 유사도 사용
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core import GPTVectorStoreIndex
# 라마인덱스, faiss 연동
from llama_index.core import StorageContext, GPTVectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.llms.openai import OpenAI
from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector

# 스트리밍
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_openai import OpenAI

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

# sample
samples = [
    {
        'input': '자동차의 엔진 작동 원리는?',
        'output': '1. 엔진은 연료를 연소시켜 에너지를 생성합니다. \n'
                  '2. 이 에너지는 피스톤을 움직이고, 크랭크축을 회전시킵니다. \n'
                  '3. 결국, 변속기를 거쳐 바퀴에 동력이 전달됩니다.'
    },
    {
        'input': '코딩을 배우는 단계는?',
        'output': '1. 프로그래밍 언어의 문법을 익힙니다. \n'
                  '2. 간단한 프로젝트를 진행하면서 실습합니다. \n'
                  '3. 데이터 구조와 알고리즘을 학습하여 문제 해결 능력을 키웁니다.'
    },
    {
        'input': '커피가 만들어지는 과정은?',
        'output': '1. 커피 원두를 수확하고 건조시킵니다. \n'
                  '2. 원두를 로스팅하여 원하는 맛과 향을 조절합니다. \n'
                  '3. 로스팅된 원두를 분쇄한 후, 물과 함께 추출하여 커피를 만듭니다.'
    },
    {
        'input': '비밀의 방에 있는 물건은?',
        'output': '1. 비밀의 방은 마법으로 보호되어 있습니다. \n'
                  '2. 그 안에는 바실리스크라는 거대한 뱀이 숨어 있습니다. \n'
                  '3. 이 방은 슬리데린의 후계자가 직접 조종할 수 있는 공간입니다.'
    },
    {
        'input': '날씨가 변하는 원인은?',
        'output': '1. 지구의 대기는 태양으로부터 에너지를 받습니다. \n'
                  '2. 이 에너지가 지역에 따라 다르게 전달되어 기압이 변합니다. \n'
                  '3. 기압 차이에 의해 바람이 발생하고, 구름과 강수량이 변화합니다.'
    },
    {
        'input': '지구가 자전하는 이유는?',
        'output': '1. 태양계 형성 당시의 각운동량이 보존되었기 때문입니다. \n'
                  '2. 외부의 힘이 크게 작용하지 않으면 회전은 지속됩니다. \n'
                  '3. 이러한 자전으로 인해 낮과 밤이 생기며, 지구의 기후와 환경이 형성됩니다.'
    },
    {
        'input': '식물이 광합성을 하는 과정은?',
        'output': '1. 식물은 잎의 엽록체에서 빛 에너지를 흡수합니다. \n'
                  '2. 이 에너지를 이용하여 이산화탄소와 물을 포도당과 산소로 변환합니다. \n'
                  '3. 생성된 포도당은 식물의 에너지원으로 사용되며, 산소는 대기 중으로 방출됩니다.'
    },
    {
        'input': '비행기가 뜨는 원리는?',
        'output': '1. 비행기의 날개는 양력을 생성하도록 설계되어 있습니다. \n'
                  '2. 빠르게 이동하면서 날개 위의 공기 흐름이 아래보다 빨라져 압력이 낮아집니다. \n'
                  '3. 이 압력 차이로 인해 비행기는 위로 떠오르게 됩니다.'
    },
    {
        'input': '컴퓨터가 부팅되는 과정은?',
        'output': '1. 전원을 켜면 CPU가 ROM에서 BIOS를 실행합니다. \n'
                  '2. BIOS가 하드웨어를 초기화하고 운영체제를 로드합니다. \n'
                  '3. 운영체제가 메모리에 로드되면, 사용자 인터페이스가 활성화되어 사용자가 조작할 수 있습니다.'
    },
    {
        'input': '사람이 숨을 쉬는 과정은?',
        'output': '1. 폐는 공기 중의 산소를 흡입합니다. \n'
                  '2. 산소는 혈액을 통해 신체 각 부분으로 전달됩니다. \n'
                  '3. 이산화탄소는 다시 폐로 이동하여 밖으로 배출됩니다.'
    }
]






# ✅ 스트리밍 가능한 GPT 모델 생성 (핸들러 제거)
stream_llm = OpenAI(
    streaming=True,
    verbose=True,
    temperature=0.5
)

# ✅ Few-Shot Learning 예제를 프롬프트로 변환
def create_few_shot_prompt(user_input):
    example_text = "\n".join([f"입력: {ex['input']}\n출력: {ex['output']}" for ex in samples])
    prompt = f"예제:\n{example_text}\n\n사용자 질문: {user_input}\n답변:"
    return prompt

# ✅ 스트리밍 방식으로 GPT 실행 (Few-Shot Learning 포함)
def stream_response(user_input):
    prompt = create_few_shot_prompt(user_input)  # Few-Shot 예제 포함 프롬프트 생성
    print("\n[🔄 Streaming 시작]\n")
    response = ""  # 최종 결과를 저장할 변수
    for chunk in stream_llm.stream(prompt):  
        response += chunk  # ✅ 반복되는 문제 방지
        print(chunk, end="", flush=True)  # ✅ 실시간 출력
    print("\n[✅ Streaming 완료]")
    return response


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
# llm = OpenAI(model="gpt-4o-mini")


# 7. MMR (Max Marginal Relevance) 기반 예제 선택 기능 추가 
# GPT가 답변을 만들때 참고할 few-shot Learning 예제 3개를 선택
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples=samples, # 샘플
    embeddings=OpenAIEmbeddings(), # 임베딩 처리용 토크나이저용도
    vectorstore_cls=FAISS, # 백터 디비, 유사도 계산을 사용할 수 있는 제품
    k = 3 # 답변 예시는 3개로 제한 (샘플이 n개이므로 다양성 고려 유사도 기준 3개만 선정)
)


# 8. mmr을 적용하여 faiss 벡터 DB에서 관련 문서 3개 검색
retriever = index.as_retriever(search_type="mmr", search_kwargs={"k": 3})
# print(retriever) # <llama_index.core.indices.vector_store.retrievers.retriever.VectorIndexRetriever object at 0x0000026519257B60>
query = "비밀의 방에 있는 물건은?"
retriever_docs = retriever.retrieve(query)
# print(retriever_docs) # [NodeWithScore(node=TextNode(id_='8980f2.... ) ) ]

# 9. 프롬프트 생성 Few-Shot + 검색된 문서 + 질문을 조합
selected_examples = example_selector.select_examples({"input": query})  # ✅ 유사한 예제 선택
example_text = "\n".join([f"입력: {ex['input']}\n출력: {ex['output']}" for ex in selected_examples])  # ✅ 예제 텍스트 생성
context = "\n".join([doc.text for doc in retriever_docs])
prompt = f"예제:\n{example_text}\n\n문맥: {context}\n\n질문: {query}\n답변:"
print(prompt)

# 10. 지피티에게입력

# ✅ 실행 (Few-Shot + 스트리밍)
response = stream_response(query)