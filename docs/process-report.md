# Báo cáo quá trình xây dựng và khắc phục lỗi hệ thống RAG

**Dự án:** hệ thống Hỏi-Đáp (RAG) trên tài liệu kỹ năng (`Skills.md`) bằng Supabase, LangChain và LLM, ưu tiên tối ưu chi phí từ tài khoản đã nạp tiền.

**Môi trường:** Windows, Python 3.12, Cursor/VS Code, PowerShell.

Mã nguồn tương ứng nằm trong [`rag-example/`](../rag-example/). Skill tổng hợp nằm trong [`skills/`](../skills/).

---

## Tóm tắt

| Mục | Kết quả |
|---|---|
| Nguồn dữ liệu | 3 file `.md` trong `skills_data/` |
| Kết quả nạp | 3 file thành 28 đoạn vector |
| Embedding | OpenAI `text-embedding-3-small` |
| Vector DB | Supabase (bảng `documents`, hàm `match_documents`) |
| LLM trả lời | OpenAI `gpt-4o-mini` |
| Quyết định quan trọng | Bỏ Anthropic sau lỗi 400 và 404, chuyển sang OpenAI |
| Nghiệm thu | Hệ thống trả lời "tài liệu chưa cập nhật" khi thiếu dữ liệu, không bịa |

---

## Giai đoạn 0: Cài Python và môi trường ảo (venv)

### Vấn đề 1: Terminal không nhận lệnh `python`

- **Tình trạng:** sau khi cài Python 3.12, gõ `python --version` hoặc `python` trong terminal của Cursor/VS Code thì báo *command not found*.
- **Nguyên nhân:** khi chạy file cài `.exe`, quên tích ô **Add Python 3.12 to PATH** ở màn hình đầu tiên, nên Windows không biết đường dẫn tới file thực thi.
- **Khắc phục:** chạy lại file cài đặt, chọn **Modify**, bắt buộc tích **Add Python.exe to PATH**, rồi khởi động lại Cursor.

### Vấn đề 2: Không kích hoạt được venv

- **Tình trạng:** đã tạo venv bằng `python -m venv venv`, nhưng gọi `venv\Scripts\activate` thì báo lỗi đỏ *running scripts is disabled on this system*.
- **Nguyên nhân:** chính sách Execution Policy mặc định của Windows PowerShell chặn việc chạy script bên ngoài.
- **Khắc phục:**
  1. Mở PowerShell với quyền Administrator.
  2. Chạy `Set-ExecutionPolicy Unrestricted -Force`.
  3. Quay lại terminal của Cursor và chạy lại `venv\Scripts\activate`. Thành công khi đầu dòng có `(venv)`.
- **Lưu ý:** `Unrestricted` là mức rất rộng. Cách an toàn hơn và không cần quyền admin: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

---

## Giai đoạn 1: Xử lý dữ liệu và vector hóa (`1_push_data.py`)

### Vấn đề định dạng file nguồn

- **Tình trạng:** 3 file tải về bị trùng tên (`SKILL`, `SKILL (2)`, `SKILL (3)`), Windows ẩn đuôi `.md` và các file còn nằm trong một file `.zip`.
- **Khắc phục:** giải nén, chuyển 3 file vào thư mục đích `skills_data/`. Nên đổi tên mỗi file thành tên có nghĩa, khác nhau.

### Chạy nạp dữ liệu

Script: [`rag-example/1_push_data.py`](../rag-example/1_push_data.py). Thông số: `chunk_size=1000`, `chunk_overlap=100`.

Log chạy thực tế:

```
(venv) PS <thư-mục-dự-án>> python 1_push_data.py
Đang quét và đọc toàn bộ các file trong thư mục skills_data...
Đã tìm thấy 3 file và phân thành 28 đoạn Vector.
Đang chuyển sang Vector và đẩy lên Supabase...
Đã nạp thành công toàn bộ các file Skill lên Supabase!
```

---

## Giai đoạn 2: Tạo kịch bản chat (`2_chat.py`)

### Vấn đề 1: `[Errno 2] No such file or directory`

- **Nguyên nhân:** file `2_chat.py` chưa tồn tại.
- **Khắc phục:** tạo file thật bằng PowerShell rồi mới dán code:

```powershell
New-Item -ItemType File -Name 2_chat.py
```

### Vấn đề 2: `ModuleNotFoundError: langchain.chains`

- **Nguyên nhân:** kiến trúc LangChain mới đã tách phần `chains` sang gói khác.
- **Khắc phục:** cài thêm gói và dùng khối `try...except` khi import:

```powershell
pip install langchain langchain-classic
```

---

## Giai đoạn 3: Lỗi API của Claude (Anthropic)

### Vấn đề 1: Lỗi tham số `temperature` (Error code: 400)

- **Lỗi:** `temperature: Extra inputs are not permitted`.
- **Nguyên nhân:** thư viện `langchain-anthropic` truyền một tham số mà phiên bản API mới không chấp nhận.
- **Khắc phục:** xóa tham số `temperature=0.7` khỏi constructor `ChatAnthropic`.

### Vấn đề 2: Lỗi định danh model (Error code: 404)

- **Lỗi:** `not_found_error` với `model: claude-3-5-sonnet-20240620` và các tên khác.
- **Kết luận của dự án:** khóa `ANTHROPIC_API_KEY` trong `.env` không thuộc mạng lưới chính hãng của Anthropic.
- **Quyết định:** chuyển sang OpenAI `gpt-4o-mini`, vì khóa OpenAI đã cấu hình và nạp tiền thành công.
- **Ghi chú:** ngoài nguyên nhân khóa, tên model cũ cũng có thể đã không còn được hỗ trợ. Nếu quay lại dùng Claude, hãy lấy khóa từ console.anthropic.com và dùng tên model hiện hành trong tài liệu của Anthropic.

---

## Giai đoạn 4: Chuyển sang OpenAI và nghiệm thu

Script hoàn chỉnh: [`rag-example/2_chat.py`](../rag-example/2_chat.py), dùng `ChatOpenAI(model="gpt-4o-mini", temperature=0.3)` và truy xuất `k=3` đoạn.

System prompt yêu cầu AI chỉ trả lời dựa trên ngữ cảnh, và nếu thiếu thông tin thì báo rằng tài liệu chưa cập nhật phần đó.

### Nghiệm thu lần 1 (chưa có dữ liệu Base44)

```
Bạn: Base44 có tính năng học skills từ file upload không?
AI đang truy xuất thông tin từ Supabase...

Phản hồi:
Tài liệu hiện chưa cập nhật phần này.
```

**Đánh giá:** hệ thống hoạt động đúng về mặt kỹ thuật. Không còn lỗi API. System prompt phát huy tác dụng: vì dữ liệu gốc chưa có thông tin về Base44, AI không bịa mà báo đúng là tài liệu chưa cập nhật.

---

## Giai đoạn 5: Bản chất RAG và cập nhật dữ liệu

RAG chỉ thông minh bằng lượng dữ liệu đã nạp. Việc AI trả lời "chưa cập nhật" ở giai đoạn 4 là do chưa đưa kiến thức chuyên ngành vào `skills_data/`, không phải lỗi code.

Quy trình hoàn thiện:

1. **Bổ sung dữ liệu** vào `skills_data/`: thêm nội dung kiến thức Base44 (xem [`skills_data/base44-knowledge-vi.md`](../rag-example/skills_data/base44-knowledge-vi.md)).
2. **Cập nhật vector DB:** chạy lại `python 1_push_data.py`.
3. **Kiểm tra:** chạy lại `python 2_chat.py` và hỏi lại câu *"Base44 có tính năng học skills từ file upload không?"*. Lần này AI phải trích được thông tin từ các đoạn vector mới nạp.

**Cảnh báo khi nạp lại:** `from_documents` chỉ thêm mới, không xóa dữ liệu cũ. Chạy lại nhiều lần sẽ tạo vector trùng. Trước khi nạp lại, nên xóa dữ liệu cũ trong Supabase SQL Editor (chỉ khi bạn chắc chắn muốn xóa toàn bộ):

```sql
truncate table documents;
```

---

## Bài học rút ra

- Cài Python nhớ tích **Add to PATH**.
- Với PowerShell, ưu tiên `RemoteSigned -Scope CurrentUser` thay vì `Unrestricted`.
- Đặt tên file nguồn có nghĩa và kiểm tra đuôi `.md` thật.
- Khi LLM trả "chưa cập nhật", kiểm tra dữ liệu nạp trước khi nghi ngờ code.
- Không bao giờ commit `.env`. Khóa `SUPABASE_SERVICE_KEY` có toàn quyền với database.
