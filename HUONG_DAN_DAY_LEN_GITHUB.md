# Đẩy repo lên GitHub (làm 1 lần, khoảng 10 phút)

Repo đã sẵn sàng trong thư mục `dagostino-legal-amlctf-suite/` (hoặc giải nén file zip cùng tên).


## Cách nhanh nhất: kéo thả lên GitHub (không cần cài Git)

1. Giải nén file zip. Bạn sẽ thấy các file `app.py`, `README.md`, `requirements.txt` và các thư mục `core`, `views`, `docs`, `tests`, `screenshots`.
2. Trên GitHub bấm **New repository** → đặt tên `dagostino-legal-amlctf-suite` → **Public** → **Create repository**.
3. Ở repo vừa tạo bấm **Add file → Upload files**. Mở thư mục vừa giải nén, bấm `Ctrl+A` (Mac: `Cmd+A`) chọn **tất cả file và thư mục bên trong**, rồi kéo thả vào khung upload.
   - Kéo *các file bên trong*, đừng kéo cả thư mục mẹ. Nếu kéo cả thư mục mẹ thì `app.py` sẽ nằm sâu một cấp và Streamlit sẽ không tìm thấy.
4. Bấm **Commit changes**. Kiểm tra trang chính repo phải thấy `app.py` và `requirements.txt` nằm ngay ngoài cùng.
5. Deploy: share.streamlit.io → **New app** → chọn repo, branch `main`, Main file `app.py` → Deploy.

**Lưu ý về 2 thư mục ẩn.** GitHub bỏ qua các thư mục bắt đầu bằng dấu chấm khi kéo thả, nên `.streamlit` và `.github` thường sẽ không lên. App vẫn chạy và vẫn đúng giao diện tối (mình đã kiểm tra bằng cách xoá hẳn 2 thư mục này rồi chạy lại). Nếu muốn có đủ, tạo tay sau khi upload:

- Bấm **Add file → Create new file**, gõ tên file là `.streamlit/config.toml` (gõ dấu `/` GitHub sẽ tự tạo thư mục), dán nội dung:

```toml
[theme]
base = "dark"
primaryColor = "#b5d334"
backgroundColor = "#0b0c0e"
secondaryBackgroundColor = "#1e2125"
textColor = "#eef0f2"
font = "sans serif"

[browser]
gatherUsageStats = false
```

- Muốn có dấu tích xanh CI trong tab Actions thì làm tương tự với file `.github/workflows/ci.yml` (nội dung nằm trong thư mục đã giải nén).

Nếu bạn quen dùng Git thì làm theo cách bên dưới, đầy đủ hơn.

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
- Tab **Actions**: workflow "CI" phải chạy xong với dấu tích xanh (119 test). Nếu đỏ, mở lên xem log và gửi lại mình.
- Trang chính repo: README hiện ảnh chụp màn hình đầy đủ.
- Ô **About** (bánh răng bên phải): dán mô tả, ví dụ
  `AML/CTF compliance suite for a fictional law firm: KYC risk rating, transaction monitoring, alert triage, SMR reporting, UBO network. Python · Streamlit · Plotly.`
  và thêm topics: `aml`, `compliance`, `streamlit`, `python`, `data-visualization`, `regtech`.
- Trên hồ sơ cá nhân GitHub: **Customize your pins** → ghim repo này.

## Bước 4 (tùy chọn nhưng nên làm) — Có link demo chạy trực tiếp
1. Vào share.streamlit.io → đăng nhập bằng GitHub → **New app**.
2. Chọn repo, nhánh `main`, file `app.py`, Python 3.12.
3. Lấy URL app, dán vào đầu README dưới dạng `**Live demo:** https://...` rồi commit.

## Nếu Streamlit Cloud báo "Oh no. Error running app."

App chạy được ở máy nhưng lỗi trên Cloud thì gần như luôn là do cài thư viện, không phải do code. Cách xử lý:

1. Mở app trên share.streamlit.io → góc dưới bên phải bấm **Manage app** → xem **log** màu đỏ. Dòng cuối cùng mới là nguyên nhân thật.
2. Các lỗi hay gặp và cách sửa:

| Log ghi | Nguyên nhân | Cách sửa |
|---|---|---|
| `ModuleNotFoundError: No module named 'docx'` | Bản trên GitHub còn `requirements.txt` cũ, chưa có `python-docx` | Đẩy lại repo mới nhất, rồi **Reboot app** |
| `Could not find a version that satisfies the requirement pandas...` / `ERROR: No matching distribution` | Python của app quá cũ so với phiên bản thư viện | Manage app → **Settings → Python version → 3.12** → Save → Reboot |
| `installer returned a non-zero exit code` | Cài thư viện thất bại (thường do 2 nguyên nhân trên) | Sửa như trên rồi Reboot |
| `ModuleNotFoundError: No module named 'core'` | Chọn sai file khi tạo app | Main file phải là `app.py` ở thư mục gốc repo |

3. Sau khi sửa: **Manage app → Reboot app**. Nếu vẫn lỗi, bấm **Delete app** rồi tạo lại New app (repo, branch `main`, file `app.py`, Python 3.12).

`requirements.txt` hiện đã hạ mức tối thiểu xuống Streamlit 1.49 / pandas 2.2 / numpy 1.26 / plotly 5.24 và app đã được chạy thử với đúng các phiên bản cũ này, nên Cloud cài được ở cả Python 3.11, 3.12 và 3.13.

## Trước khi gửi cho HR, hãy kiểm tra
- Dòng cuối README ghi tên **Brian Phu** và LICENSE ghi tên đó: mình lấy từ tên hiển thị trong dashboard. Sửa nếu không đúng tên bạn.
- Tên khách hàng/thực thể trong dữ liệu mẫu (kể cả tên quốc gia trong phần "foreign dimension") đều là hư cấu, để tránh nhắc đến quốc gia thật. Nếu muốn đổi, sửa `core/ref.py`.
- README có mục **Development notes** ghi rõ dự án được phát triển với sự hỗ trợ của AI. Nên giữ, và hãy đọc `docs/METHODOLOGY.md` để tự giải thích được các công thức (mô hình rủi ro 4 yếu tố AUSTRAC, cách sinh cảnh báo theo typology, công thức của Simulator) nếu được hỏi phỏng vấn.
- Dự án này là bản đồng hành (companion) của dashboard tài chính `dagostino-legal-fa-dashboard` — nếu bạn đã đẩy dashboard đó lên GitHub, hai repo này nên được ghim cạnh nhau trên hồ sơ để thể hiện rõ cùng một "firm" giả định.
