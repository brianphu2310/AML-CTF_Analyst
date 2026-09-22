# Đẩy repo lên GitHub (làm 1 lần, khoảng 10 phút)

Repo đã sẵn sàng trong thư mục `dagostino-legal-amlctf-suite/` (hoặc giải nén file zip cùng tên).

## Bước 1 — Tạo repo rỗng trên GitHub
1. Vào github.com → nút **+** (góc trên phải) → **New repository**.
2. Repository name: `dagostino-legal-amlctf-suite`
3. Chọn **Public** (HR mới xem được).
4. **Không** tick "Add a README", "Add .gitignore" hay "Choose a license" (repo đã có sẵn cả ba).
5. Bấm **Create repository**.

## Bước 2 — Đẩy code lên (dùng Terminal / Git Bash)
Thay `TEN-GITHUB-CUA-BAN` bằng username GitHub của bạn:

```bash
cd dagostino-legal-amlctf-suite
git init -b main
git config user.name "Tên của bạn"
git config user.email "email-đăng-ký-github-của-bạn"
git add .
git commit -m "Initial commit: D'Agostino Legal AML/CTF compliance suite"
git remote add origin https://github.com/TEN-GITHUB-CUA-BAN/dagostino-legal-amlctf-suite.git
git push -u origin main
```
Dùng đúng email đã đăng ký GitHub (hoặc email dạng `...@users.noreply.github.com` trong Settings → Emails) thì commit mới hiện trên hồ sơ của bạn.

> Không nên kéo-thả thư mục lên web GitHub: nó có thể bỏ sót các file ẩn như `.github/workflows/ci.yml` và `.gitignore`.

## Bước 3 — Kiểm tra sau khi đẩy
- Tab **Actions**: workflow "CI" phải chạy xong với dấu tích xanh (70 test). Nếu đỏ, mở lên xem log và gửi lại mình.
- Trang chính repo: README hiện ảnh chụp màn hình đầy đủ.
- Ô **About** (bánh răng bên phải): dán mô tả, ví dụ
  `AML/CTF compliance suite for a fictional law firm: KYC risk rating, transaction monitoring, alert triage, SMR reporting, UBO network. Python · Streamlit · Plotly.`
  và thêm topics: `aml`, `compliance`, `streamlit`, `python`, `data-visualization`, `regtech`.
- Trên hồ sơ cá nhân GitHub: **Customize your pins** → ghim repo này.

## Bước 4 (tùy chọn nhưng nên làm) — Có link demo chạy trực tiếp
1. Vào share.streamlit.io → đăng nhập bằng GitHub → **New app**.
2. Chọn repo, nhánh `main`, file `app.py`, Python 3.12.
3. Lấy URL app, dán vào đầu README dưới dạng `**Live demo:** https://...` rồi commit.

## Trước khi gửi cho HR, hãy kiểm tra
- Dòng cuối README ghi tên **Brian Phu** và LICENSE ghi tên đó: mình lấy từ tên hiển thị trong dashboard. Sửa nếu không đúng tên bạn.
- Tên khách hàng/thực thể trong dữ liệu mẫu (kể cả tên quốc gia trong phần "foreign dimension") đều là hư cấu, để tránh nhắc đến quốc gia thật. Nếu muốn đổi, sửa `core/ref.py`.
- README có mục **Development notes** ghi rõ dự án được phát triển với sự hỗ trợ của AI. Nên giữ, và hãy đọc `docs/METHODOLOGY.md` để tự giải thích được các công thức (mô hình rủi ro 4 yếu tố AUSTRAC, cách sinh cảnh báo theo typology, công thức của Simulator) nếu được hỏi phỏng vấn.
- Dự án này là bản đồng hành (companion) của dashboard tài chính `dagostino-legal-fa-dashboard` — nếu bạn đã đẩy dashboard đó lên GitHub, hai repo này nên được ghim cạnh nhau trên hồ sơ để thể hiện rõ cùng một "firm" giả định.
