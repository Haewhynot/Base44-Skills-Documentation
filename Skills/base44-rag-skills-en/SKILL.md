---
name: base44-rag-skills-en
description: >
  Guide for building, operating and debugging a RAG (Q&A) system over the `skills_data/` folder (containing Skills.md / SKILL.md files about Base44) using Python 3.12 + venv, LangChain, Supabase (pgvector) and OpenAI (text-embedding-3-small + gpt-4o-mini). Also holds the reference knowledge on how Base44 handles its Knowledge Base and Super Agent Skills. MUST be used when the user mentions: RAG, vector, embedding, Supabase documents / match_documents, 1_push_data.py, 2_chat.py, skills_data, loading skills into a vector DB, chatting with skill documents, Base44 SDK / CLI, "can Base44 learn skills from uploaded files", or hits errors such as venv / PowerShell Execution Policy / ModuleNotFoundError langchain.chains / Anthropic 400 temperature / 404 model, even when they never say the word "RAG". Use for Claude Code, Cursor, the VS Code Claude Code extension and Codex.
---

# Base44 RAG Skills (English)

Standard reference for AI assistants (Claude Code, Cursor, the Claude Code extension for VS Code, Codex, Qoder) covering two things:

1. **Knowledge**: how Base44 handles "learning data" versus "learning skills" (section 3).
2. **Tested process**: how the RAG system was built, run and debugged, so an agent can repeat it exactly instead of guessing (section 4 onward).

> Ground rule: answer only from this skill and from the contents of `skills_data/`. Never invent Base44 functions, parameters or features. If the information is missing, say the documentation has not been updated for that part.

---

## 1. When to read this skill

| Group | Example user requests |
|---|---|
| Build RAG | "load the skills into Supabase", "build a chat over the skill files" |
| Operate RAG | "add a new document", "re-ingest the vectors", "run the chat again" |
| Environment errors | `python` not recognized, `venv\Scripts\activate` blocked |
| LangChain / API errors | `langchain.chains` not found, Anthropic 400 / 404 |
| Base44 knowledge | "Can Base44 learn skills from an uploaded file?", using base44-sdk / base44-cli with an IDE |

---

## 2. Folder structure (the folder the RAG points to)

```
D:\claude-skills-rag\                  <- project root (Windows)
├── venv\                              <- Python 3.12 virtual environment (do not commit)
├── skills_data\                       <- THE DATA FOLDER THE RAG POINTS TO
│   ├── <meaningful-name-1>.md         <- e.g. base44-sdk.md
│   ├── <meaningful-name-2>.md         <- e.g. base44-cli.md
│   └── <meaningful-name-3>.md         <- e.g. base44-skills-documentation.md
├── 1_push_data.py                     <- read skills_data -> split -> embed -> push to Supabase
├── 2_chat.py                          <- terminal RAG chat loop
├── .env                               <- secrets (DO NOT commit)
├── .gitignore                         <- must contain: venv/, .env
└── SKILL.md (or the copy under .claude/skills/...)  <- this file
```

Mandatory conventions:

- `skills_data/` is the **single source of truth**. To make the AI know something new, add a `.md` file here and re-ingest (section 4, Phase 5).
- Files must have a real `.md` extension. In the original project, the 3 downloaded files had duplicate names (`SKILL`, `SKILL (2)`, `SKILL (3)`), Windows hid the extension, and they were stuck inside a `.zip`. Unzip them and give each a **distinct, meaningful name**.
- Supabase table name: `documents`. Search function: `match_documents`. These two names must match between Supabase and both scripts.

Variables in `.env`:

```
SUPABASE_URL=...
SUPABASE_SERVICE_KEY=...
OPENAI_API_KEY=...
```

`SUPABASE_SERVICE_KEY` has full access to the database. Never print it to logs, commit it, or paste it into a chat.

---

## 3. Background knowledge: how Base44 handles data and skills

Base44 clearly separates **learning Knowledge** from **learning action Skills**.

### 3.1. Knowledge Base (learning knowledge)

- Capability: **YES**, it learns directly from uploaded files.
- Formats: text documents (PDF, Word, TXT, etc.).
- How it works: upload documents into the Knowledge Base of the AI Chatbot integrated in a Base44 app. The AI reads, scans and learns from them to answer end-user questions automatically.

### 3.2. Super Agent Skills (learning action skills)

- Capability: **mainly through prompts (descriptive text)**. It does **not currently support** uploading a logic-structure file (JSON or MD containing logic) for the agent to convert into an executable skill automatically.
- "Super Agents" run in the background 24/7 to automate complex workflows. To teach a new skill or set operating rules, you must describe the work in text.

### 3.3. Practical use of Agent Skills files

In the Base44 developer community, "uploading skills" is about improving the **developer experience (DX)**, not injecting them into the Base44 platform.

- Nature: files such as `SKILL.md` are pre-optimized documentation sets containing `base44-sdk` or `base44-cli` context.
- Deployment: load them into the workspace of an AI IDE/assistant, not into Base44.
  - Cursor: Project Knowledge or the `.cursorrules` file (or `.cursor/rules/*.mdc` in newer versions).
  - Claude / Qoder: Project Knowledge / context window.
- Benefits:
  1. Teaches the AI the real structure of the Base44 framework.
  2. Generates code that follows Base44 SDK/CLI standards.
  3. Anti-hallucination: reduces the AI inventing functions that do not exist.
  4. Helps with API integrations: Supabase, GitHub, Drive API, Google Calendar API.

Sections 3.1 and 3.2 are exactly the content that must live in `skills_data/` so the RAG can answer "Can Base44 learn skills from uploaded files?" (see Phase 5).

---

## 4. RAG build process (in order)

### Phase 0: Python and venv (Windows)

Requirement: Python 3.12.

```powershell
python --version                 # must print Python 3.12.x
python -m venv venv
venv\Scripts\activate            # success when (venv) appears at the start of the prompt
pip install python-dotenv supabase langchain langchain-classic langchain-community langchain-openai langchain-text-splitters
```

The package list above is inferred from the `import` lines in the two scripts. If the project has a `requirements.txt`, prefer that. Once everything works, run `pip freeze > requirements.txt`.

The two common errors in this phase are in section 5 (E1, E2).

### Phase 1: Prepare data and load vectors (`1_push_data.py`)

1. Unzip the source files, rename them meaningfully, and place them in `skills_data/` (`.md` extension).
2. Make sure Supabase already has the `documents` table and the `match_documents` function (see 4.1).
3. Run `python 1_push_data.py`.

Expected result (real log from the project, 3 files into 28 chunks):

```
(venv) PS D:\claude-skills-rag> python 1_push_data.py
⏳ Scanning and reading all files in skills_data...
✅ Found 3 files and split them into 28 vector chunks.
⏳ Converting to vectors and pushing to Supabase...
🎉 SUCCESS! All skill files were loaded into Supabase!
```

Parameters used: `chunk_size=1000`, `chunk_overlap=100`, embedding model `text-embedding-3-small`.

Source of `1_push_data.py`:

```python
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
    raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in the .env file!")

supabase: Client = create_client(supabase_url, supabase_key)

folder_path = "skills_data"
print("⏳ Scanning and reading all files in skills_data...")

loader = DirectoryLoader(
    folder_path,
    glob="**/*",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
raw_docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(raw_docs)

print(f"✅ Found {len(raw_docs)} files and split them into {len(docs)} vector chunks.")

print("⏳ Converting to vectors and pushing to Supabase...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = SupabaseVectorStore.from_documents(
    docs,
    embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
)

print("🎉 SUCCESS! All skill files were loaded into Supabase!")
```

Notes when editing the script:

- `glob="**/*"` reads every file in `skills_data/`. If binary files (zip, pdf, images) are mixed in, `TextLoader` will fail. Keep only UTF-8 text files. You may change it to `glob="**/*.md"` to be safe.
- `from_documents` **adds** rows and never removes old ones. Running it repeatedly creates **duplicate vectors** (see error E9).
- The Vietnamese console strings of the original script were translated to English here. This does not change behavior.

#### 4.1. Prepare Supabase (prerequisite)

The original report does not record this step because the table already existed. This is the standard LangChain template for `text-embedding-3-small` (1536 dimensions). Run it in the Supabase SQL Editor if the table or function does not exist:

```sql
create extension if not exists vector;

create table if not exists documents (
  id bigserial primary key,
  content text,
  metadata jsonb,
  embedding vector(1536)
);

create or replace function match_documents (
  query_embedding vector(1536),
  match_count int default null,
  filter jsonb default '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where documents.metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;
```

If you switch to an embedding model with a different dimension (for example 3072), change `vector(1536)` and re-ingest everything.

### Phase 2: Create `2_chat.py`

- `[Errno 2] No such file or directory` means the file does not exist yet. Create the real file first, then paste the code:

```powershell
New-Item -ItemType File -Name 2_chat.py
```

- If `import langchain.chains` fails, see error E4.

### Phase 3: Trying Claude (Anthropic) and why the project moved to OpenAI

The project first tried `langchain-anthropic` and hit two errors (E5, E6 in section 5). **Final decision: use OpenAI `gpt-4o-mini`**, because the OpenAI key was already configured and funded, which keeps cost low. This is the working configuration. Do not change it unless the user asks.

### Phase 4: Complete source and acceptance test (`2_chat.py`)

```python
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
    "You are an expert AI assistant. "
    "Use the context provided below to answer the user's question accurately and concisely. "
    "If the information is not in the context, say that the documentation has not been updated for this part yet.\n\n"
    "Document context:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

print("=" * 60)
print("🤖 RAG SYSTEM READY (using OpenAI gpt-4o-mini)")
print("Type your question and press Enter. Type 'exit' to stop.")
print("=" * 60 + "\n")

while True:
    try:
        user_input = input("👤 You: ")
        if user_input.lower().strip() in ["exit", "quit"]:
            break
        if not user_input.strip():
            continue

        print("⏳ The AI is retrieving information from Supabase...")
        response = rag_chain.invoke({"input": user_input})

        print(f"\n💡 Answer:\n{response['answer']}\n")
        print("-" * 60)
    except KeyboardInterrupt:
        break
```

Key parameters: `k=3` (chunks retrieved), `temperature=0.3`, the `try/except` import block that works with both LangChain architectures, and a system prompt that forces the answer "documentation has not been updated for this part" when information is missing. The original system prompt was in Vietnamese and made the bot answer in Vietnamese; this English version answers in English.

Acceptance test, run 1 (no Base44 data in `skills_data/` yet):

```
👤 You: Can Base44 learn skills from uploaded files?
⏳ The AI is retrieving information from Supabase...

💡 Answer:
The documentation has not been updated for this part yet.
```

This is the **correct result**: no API error, and the system prompt stops the AI from making things up when data is missing.

### Phase 5: What RAG really is, and updating data

RAG is only as smart as the data loaded into it. A "not updated" answer means data is missing, not that the code is broken.

Standard update procedure:

1. Add or edit a `.md` file in `skills_data/` (for example, copy sections 3.1, 3.2 and 3.3 of this skill into a file).
2. **Delete the old vectors** to avoid duplicates (see E9), then re-ingest: `python 1_push_data.py`.
3. Run `python 2_chat.py` and ask again: "Can Base44 learn skills from uploaded files?"
4. A correct answer must say: the Knowledge Base **can** learn from uploaded files (PDF, Word, TXT); Super Agent Skills work **mainly through prompts** and do not yet accept uploaded logic files directly.

---

## 5. Error table (seen so far, with fixes)

| ID | Symptom | Cause | Fix |
|---|---|---|---|
| E1 | `python --version` says command not found | "Add Python to PATH" was not ticked during install | Re-run the installer, choose **Modify**, tick **Add Python.exe to PATH**, restart Cursor/VS Code |
| E2 | `venv\Scripts\activate`: *running scripts is disabled on this system* | PowerShell Execution Policy blocks scripts | Open PowerShell **Run as Administrator** and run `Set-ExecutionPolicy Unrestricted -Force` (what the project used). Safer option, no admin needed: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. Success when `(venv)` appears |
| E3 | `[Errno 2] No such file or directory` when running `2_chat.py` | The file has not been created | `New-Item -ItemType File -Name 2_chat.py`, then paste the code |
| E4 | `ModuleNotFoundError: langchain.chains` | The newer LangChain architecture moved `chains` to another package | `pip install langchain langchain-classic` and use the `try/except` import block (already in 2_chat.py) |
| E5 | Anthropic `Error code: 400`: `temperature: Extra inputs are not permitted` | `langchain-anthropic` passes a parameter the API no longer accepts | Remove `temperature=...` from the `ChatAnthropic` constructor |
| E6 | Anthropic `Error code: 404` `not_found_error` with `model: claude-3-5-sonnet-20240620` and other names | The project concluded the `ANTHROPIC_API_KEY` in `.env` was not an official Anthropic key. It is also worth checking that the model name is still supported | The project switched to OpenAI `gpt-4o-mini`. To return to Claude, use a key from console.anthropic.com and a current model name from Anthropic's docs |
| E7 | Source files share a name, lack the `.md` extension, and are stuck in a `.zip` | Several same-name downloads; Windows hides extensions | Unzip, show file extensions, give meaningful names, move into `skills_data/` |
| E8 | The AI answers "documentation has not been updated for this part" | No relevant data in the vector DB yet | Not an error. Add content to `skills_data/` and re-ingest |
| E9 | Repeated or duplicate chunks in results after re-ingesting | `from_documents` adds rows and never deletes old ones | In the Supabase SQL Editor run `truncate table documents;` before re-running `1_push_data.py` (only if the user agrees to delete all old data) |

---

## 6. Rules for AI assistants working on this project

Do:

- Read this skill and `skills_data/` before answering any Base44 question.
- Keep the table name `documents`, the function `match_documents` and the embedding model `text-embedding-3-small` unless the user asks to change them (and remind them to re-ingest everything).
- When documents are added, tell the user to re-run `1_push_data.py` and warn about duplicate vectors.
- When an error appears, check the table in section 5 before trying other approaches.
- Match the user's language.

Do not:

- Do not invent Base44 SDK/CLI features, functions or parameters. If information is missing, say "the documentation has not been updated for this part yet."
- Do not put `SUPABASE_SERVICE_KEY` or `OPENAI_API_KEY` in code, logs or commits.
- Do not run `truncate table documents` or delete data without explicit user consent.
- Do not re-add `temperature` to `ChatAnthropic` (it causes E5).
- Do not claim Base44 lets you upload a skill file that the agent turns into a skill automatically. It does not currently.

---

## 7. How each tool discovers this skill

Same content, placed where each tool scans for it. Project root is `D:\claude-skills-rag\`.

| Tool | Location | Notes |
|---|---|---|
| Claude Code (terminal) and the Claude Code extension for VS Code | `.claude\skills\base44-rag-skills-en\SKILL.md` (per project) or `%USERPROFILE%\.claude\skills\base44-rag-skills-en\SKILL.md` (all projects) | Reads `name` + `description` from the frontmatter to decide when to load the skill. Keep the folder name equal to `name` |
| Cursor | `.cursor\rules\base44-rag-skills-en.mdc` | Use Cursor's own frontmatter (`description`, `alwaysApply: false`) and paste the body below it. Older versions use `.cursorrules` in the project root |
| Codex | `AGENTS.md` in the project root | Put a short summary plus the line: "For RAG/Base44/skills_data, read `.claude/skills/base44-rag-skills-en/SKILL.md`." If your Codex version supports its own skills folder, check Codex's documentation for the location |
| Claude.ai / Qoder | Upload to Project Knowledge | As described in 3.3 |

PowerShell commands to create the copies from one source file (run at the project root, assuming the source is `SKILL.md`):

```powershell
New-Item -ItemType Directory -Force .claude\skills\base44-rag-skills-en | Out-Null
Copy-Item SKILL.md .claude\skills\base44-rag-skills-en\SKILL.md

New-Item -ItemType Directory -Force .cursor\rules | Out-Null
Copy-Item SKILL.md .cursor\rules\base44-rag-skills-en.mdc
```

For the `.mdc` copy, open it and change the frontmatter to:

```
---
description: RAG over skills_data (Supabase + LangChain + OpenAI) and Base44 knowledge. Use when RAG, vector, skills_data, or Base44 SDK/CLI is mentioned.
alwaysApply: false
---
```

Minimal `AGENTS.md` template for Codex:

```markdown
# Agent instructions

- This project is a RAG over the `skills_data/` folder (Python 3.12, venv, LangChain, Supabase, OpenAI).
- For anything about RAG, vector loading, Base44, or environment/LangChain/API errors, read `.claude/skills/base44-rag-skills-en/SKILL.md` first.
- Never write secret keys into code or commits. Never delete Supabase data without permission.
```

Do not install the Vietnamese and English skills side by side in the same tool, because their descriptions overlap and the agent may load both. Choose one per project, or merge them.

---

## 8. Acceptance checklist

- [ ] `python --version` prints 3.12.x and `(venv)` shows at the start of the terminal prompt
- [ ] `.env` has all 3 variables; `.gitignore` contains `venv/` and `.env`
- [ ] `skills_data/` contains only UTF-8 `.md` files with distinct, meaningful names
- [ ] Supabase has the `documents` table and the `match_documents` function (1536-dim vectors)
- [ ] `python 1_push_data.py` prints the file and chunk counts with no errors
- [ ] `python 2_chat.py` starts, answers a Base44 question correctly per section 3
- [ ] A question outside the documents gets "documentation has not been updated for this part yet"
- [ ] The skill is placed correctly for the tool you use (section 7)
