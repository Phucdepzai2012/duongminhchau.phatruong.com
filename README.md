# Trường THCS Dương Minh Châu — GitHub Pages mirror

Bản này khắc phục lỗi bản trước bằng cách đồng bộ ở GitHub Actions thay vì `fetch()` trực tiếp từ trình duyệt.

## Cấu trúc
- `index.html`: trang GitHub Pages
- `sync.py`: tải trang nguồn, thay nhận diện và tạo `synced.html`
- `.github/workflows/sync.yml`: tự chạy mỗi 30 phút và cho chạy thủ công
- `requirements.txt`: thư viện Python

## Cài trên GitHub
1. Tạo repository mới.
2. Upload toàn bộ các file/thư mục này.
3. Vào Settings → Pages → Deploy from branch → main → /root.
4. Vào Actions → Sync website → Run workflow lần đầu.

Lưu ý: `sync.py` khóa form và không chạy JavaScript của nguồn để tránh gửi dữ liệu đăng nhập trên bản mirror. Đây là bản đồng bộ/không chính thức.
