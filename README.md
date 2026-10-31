# Base44 Skills Documentation

[Tiếng Việt](#tiếng-việt) | [English](#english)

---

## Tiếng Việt

Bộ skill giúp AI coding assistant (**Claude Code**, **Cursor**, **extension Claude Code trên VS Code**, **Codex**) hiểu cách Base44 xử lý Knowledge Base và Super Agent Skills, đồng thời hướng dẫn dựng hệ thống **RAG (hỏi-đáp)** trên thư mục `skills_data/` bằng Python 3.12, LangChain, Supabase (pgvector) và OpenAI.

### Skill này giải quyết gì

- Trả lời đúng câu hỏi như "Base44 có học skill từ file upload không?" và giảm việc AI bịa hàm của Base44 SDK/CLI.
- Có sẵn quy trình dựng RAG từng bước, kèm mã nguồn `1_push_data.py` và `2_chat.py`.
- Có bảng lỗi đã gặp thực tế (PATH, PowerShell Execution Policy, `langchain.chains`, Anthropic 400/404) và cách sửa.

### Nội dung repo

| Đường dẫn | Mô tả |
|---|---|
| `skills/base44-rag-skills/SKILL.md` | Skill bản tiếng Việt |
| `skills/base44-rag-skills-en/SKILL.md` | Skill bản tiếng Anh |
| `rag-example/` | Mã nguồn mẫu: `1_push_data.py`, `2_chat.py`, `requirements.txt`, `.env.example`, `skills_data/` |
| `cursor/base44-rag-skills.mdc` | Bản rule cho Cursor |
| `AGENTS.md` | Hướng dẫn ngắn cho Codex |
| `docs/process-report.md` | Báo cáo quá trình xây dựng và khắc phục lỗi |

### Cài đặt skill

Chọn **một** bản ngôn ngữ cho mỗi dự án, vì hai bản có mô tả gần giống nhau và agent có thể nạp cả hai.

**Bước 1. Tải repo**

```powershell
git clone https://github.com/Haewhynot/Base44-Skills-Documentation.git
cd Base44-Skills-Documentation
```

**Bước 2. Chép skill vào đúng vị trí của công cụ bạn dùng**

Claude Code và extension Claude Code trên VS Code (trong dự án của bạn):

```powershell
# Bản tiếng Việt
New-Item -ItemType Directory -Force <dự-án-của-bạn>\.claude\skills\base44-rag-skills | Out-Null
Copy-Item skills\base44-rag-skills\SKILL.md <dự-án-của-bạn>\.claude\skills\base44-rag-skills\SKILL.md

# Hoặc bản tiếng Anh
New-Item -ItemType Directory -Force <dự-án-của-bạn>\.claude\skills\base44-rag-skills-en | Out-Null
Copy-Item skills\base44-rag-skills-en\SKILL.md <dự-án-của-bạn>\.claude\skills\base44-rag-skills-en\SKILL.md
```

Muốn dùng cho mọi dự án, thay `<dự-án-của-bạn>\.claude` bằng `%USERPROFILE%\.claude`.

Cursor:

```powershell
New-Item -ItemType Directory -Force <dự-án-của-bạn>\.cursor\rules | Out-Null
Copy-Item cursor\base44-rag-skills.mdc <dự-án-của-bạn>\.cursor\rules\base44-rag-skills.mdc
```

Codex: chép `AGENTS.md` vào gốc dự án của bạn. Nếu phiên bản Codex bạn dùng hỗ trợ thư mục skills riêng, hãy xem tài liệu của Codex để biết vị trí.

**Bước 3. Kiểm tra**

Mở dự án trong công cụ và hỏi: *"Base44 có học skill từ file upload không?"* hoặc *"Hướng dẫn tôi nạp thư mục skills_data lên Supabase"*. Nếu skill được nhận, câu trả lời sẽ bám theo nội dung trong `SKILL.md`.

### Chạy thử ví dụ RAG

Yêu cầu: Python 3.12, tài khoản Supabase, khóa OpenAI.

```powershell
cd rag-example
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env       # rồi điền khóa thật vào .env
python 1_push_data.py             # nạp skills_data/ lên Supabase
python 2_chat.py                  # hỏi đáp trên terminal
```

Trước khi chạy, tạo bảng `documents` và hàm `match_documents` trong Supabase theo mục 4.1 của `SKILL.md`.

**Bảo mật:** không bao giờ commit file `.env`. `SUPABASE_SERVICE_KEY` có toàn quyền với database của bạn.

### Đóng góp

Mở Issue hoặc Pull Request nếu bạn gặp lỗi mới, muốn bổ sung bản dịch hoặc vị trí cài đặt cho công cụ khác.

### Giấy phép

Phát hành theo giấy phép MIT. Xem file [LICENSE](LICENSE).

---

## English

A skill set that helps AI coding assistants (**Claude Code**, **Cursor**, the **Claude Code extension for VS Code**, **Codex**) understand how Base44 handles its Knowledge Base and Super Agent Skills. It also walks through building a **RAG (Q&A)** system over a `skills_data/` folder with Python 3.12, LangChain, Supabase (pgvector) and OpenAI.

### What it solves

- Answers questions like "Can Base44 learn skills from an uploaded file?" and reduces invented Base44 SDK/CLI functions.
- Gives a step-by-step RAG build process with the source of `1_push_data.py` and `2_chat.py`.
- Includes a table of real errors (PATH, PowerShell Execution Policy, `langchain.chains`, Anthropic 400/404) and their fixes.

### Repository contents

| Path | Description |
|---|---|
| `skills/base44-rag-skills/SKILL.md` | Vietnamese skill |
| `skills/base44-rag-skills-en/SKILL.md` | English skill |
| `rag-example/` | Sample code: `1_push_data.py`, `2_chat.py`, `requirements.txt`, `.env.example`, `skills_data/` |
| `cursor/base44-rag-skills.mdc` | Rule file for Cursor |
| `AGENTS.md` | Short instructions for Codex |
| `docs/process-report.md` | Build and debugging report |

### Install the skill

Pick **one** language version per project. The two descriptions overlap, so an agent might load both.

**Step 1. Get the repo**

```bash
git clone https://github.com/Haewhynot/Base44-Skills-Documentation.git
cd Base44-Skills-Documentation
```

**Step 2. Copy the skill to the location your tool scans**

Claude Code and the Claude Code extension for VS Code (inside your project):

```bash
mkdir -p <your-project>/.claude/skills/base44-rag-skills-en
cp skills/base44-rag-skills-en/SKILL.md <your-project>/.claude/skills/base44-rag-skills-en/SKILL.md
```

For the Vietnamese version, use the folder `base44-rag-skills` instead. To make it available in every project, replace `<your-project>/.claude` with `~/.claude`.

Cursor:

```bash
mkdir -p <your-project>/.cursor/rules
cp cursor/base44-rag-skills.mdc <your-project>/.cursor/rules/base44-rag-skills.mdc
```

Codex: copy `AGENTS.md` to your project root. If your Codex version supports its own skills folder, check Codex's documentation for the location.

**Step 3. Verify**

Open your project in the tool and ask: *"Can Base44 learn skills from an uploaded file?"* or *"Walk me through loading skills_data into Supabase."* If the skill is picked up, the answer will follow the content of `SKILL.md`.

### Try the RAG example

Requirements: Python 3.12, a Supabase account, an OpenAI key.

```bash
cd rag-example
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # then put your real keys in .env
python 1_push_data.py             # load skills_data/ into Supabase
python 2_chat.py                  # terminal Q&A
```

Before running, create the `documents` table and the `match_documents` function in Supabase using section 4.1 of `SKILL.md`.

**Security:** never commit your `.env` file. `SUPABASE_SERVICE_KEY` has full access to your database.

### Contributing

Open an Issue or Pull Request if you hit a new error, or want to add a translation or an install location for another tool.

### License

Released under the MIT License. See [LICENSE](LICENSE).
