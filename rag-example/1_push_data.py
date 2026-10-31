import os
from dotenv import load_dotenv
from supabase.client import create_client, Client
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("❌ Thiếu SUPABASE_URL hoặc SUPABASE_SERVICE_KEY trong file .env!")

supabase: Client = create_client(supabase_url, supabase_key)

folder_path = "skills_data"
print("⏳ Đang quét và đọc toàn bộ các file trong thư mục skills_data...")

loader = DirectoryLoader(
    folder_path,
    glob="**/*",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
raw_docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(raw_docs)

print(f"✅ Đã tìm thấy {len(raw_docs)} file và phân thành {len(docs)} đoạn Vector.")

print("⏳ Đang chuyển sang Vector và đẩy lên Supabase...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = SupabaseVectorStore.from_documents(
    docs,
    embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
)

print("🎉 XUẤT SẮC! Đã nạp thành công toàn bộ các file Skill lên Supabase!")
