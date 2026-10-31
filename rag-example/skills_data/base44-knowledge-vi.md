# Kiến thức về Base44: học Kiến thức và học Kỹ năng

Base44 phân biệt khá rõ tính năng tùy thuộc vào việc bạn muốn AI học Kiến thức (Knowledge) hay học Kỹ năng thao tác (Skills).

## 1. Học Kiến thức (Knowledge Base)

Base44 CÓ hỗ trợ học kiến thức từ file upload.

- Định dạng hỗ trợ: tài liệu văn bản như PDF, Word, TXT.
- Cách hoạt động: bạn upload tài liệu trực tiếp vào hệ thống Knowledge Base của AI Chatbot tích hợp trên app Base44.
- Mục đích: AI đọc, quét và học dữ liệu từ các file này để có cơ sở tự động trả lời câu hỏi của người dùng cuối.

## 2. Học Kỹ năng hành động (Super Agent Skills)

Base44 chủ yếu nhận kỹ năng qua prompt (văn bản mô tả). Hiện chưa hỗ trợ upload trực tiếp file cấu trúc logic.

- Base44 cung cấp các "Super Agents" chạy ngầm 24/7 để tự động hóa các workflow phức tạp.
- Để dạy skill mới hoặc đặt quy tắc vận hành cho agent, bạn cần mô tả công việc bằng văn bản (prompt).
- Giới hạn hiện tại: nền tảng chưa cho upload trực tiếp file cấu trúc logic (JSON hoặc MD chứa logic) để agent tự chuyển thành kỹ năng thực thi.

## 3. File Agent Skills dùng trong quá trình phát triển (DX)

Trong cộng đồng developer Base44, "upload skills" chủ yếu để nâng cao trải nghiệm lập trình, không phải nạp vào nền tảng Base44.

- File skill (ví dụ `SKILL.md`) là bộ tài liệu đã tối ưu, chứa ngữ cảnh `base44-sdk` hoặc `base44-cli`.
- Cách triển khai: nạp vào không gian làm việc của AI IDE hoặc Assistant, không upload lên Base44.
  - Cursor: dùng Project Knowledge hoặc file `.cursorrules` (hoặc `.cursor/rules/*.mdc`).
  - Claude hoặc Qoder: dùng Project Knowledge hoặc cửa sổ ngữ cảnh.

### Lợi ích khi nạp file skill vào IDE

1. Dạy AI nắm đúng cấu trúc framework Base44.
2. Sinh code đúng chuẩn Base44 SDK và CLI.
3. Chống hallucination: giảm việc AI bịa ra hàm không tồn tại.
4. Hỗ trợ tích hợp API: Supabase, GitHub, Drive API, Google Calendar API.

## 4. Hỏi nhanh

**Hỏi: Base44 có tính năng học skills từ file upload không?**
Đáp: Tùy loại. Knowledge Base thì CÓ học từ file upload (PDF, Word, TXT). Super Agent Skills thì chủ yếu qua prompt, chưa hỗ trợ upload file logic trực tiếp.

**Hỏi: Tôi nên upload file SKILL.md ở đâu?**
Đáp: Nạp vào công cụ lập trình như Cursor, Claude hoặc Qoder để AI viết code Base44 chính xác hơn. Không upload lên nền tảng Base44 để làm kỹ năng cho agent.
