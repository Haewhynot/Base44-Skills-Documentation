import os
from dotenv import load_dotenv
from supabase.client import create_client, Client
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.prompts import ChatPromptTemplate

try:
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ModuleNotFoundError:
    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

system_prompt = (
    "Bạn là một trợ lý AI chuyên gia. "
    "Dựa vào thông tin ngữ cảnh được cung cấp dưới đây để trả lời câu hỏi của người dùng một cách chính xác và ngắn gọn. "
    "Nếu thông tin không có trong ngữ cảnh, hãy thông báo rằng tài liệu hiện chưa cập nhật phần này.\n\n"
    "Ngữ cảnh tài liệu:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

print("=" * 60)
print("🤖 HỆ THỐNG RAG ĐÃ SẴN SÀNG (Đang dùng OpenAI gpt-4o-mini)")
print("Gõ câu hỏi của bạn và nhấn Enter. Gõ 'exit' hoặc 'thoát' để dừng.")
print("=" * 60 + "\n")

while True:
    try:
        user_input = input("👤 Bạn: ")
        if user_input.lower().strip() in ["exit", "quit", "thoat", "thoát"]:
            break
        if not user_input.strip():
            continue

        print("⏳ AI đang truy xuất thông tin từ Supabase...")
        response = rag_chain.invoke({"input": user_input})

        print(f"\n💡 Phản hồi:\n{response['answer']}\n")
        print("-" * 60)
    except KeyboardInterrupt:
        break
