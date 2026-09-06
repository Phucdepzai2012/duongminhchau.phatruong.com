#!/usr/bin/env python3
import re
import html as htmlmod
from urllib.parse import urljoin
from pathlib import Path
import requests
from bs4 import BeautifulSoup

SOURCE = 'http://thcsngovanso.phuonglaocai.edu.vn/'
OUT = Path('synced.html')
SCHOOL = 'Trường THCS Dương Minh Châu'
PRINCIPAL = 'Nguyễn Xuân Phúc'
OLD_SCHOOL = [
    'Trường THCS Ngô Văn Sở',
    'THCS Ngô Văn Sở',
    'THCS NGÔ VĂN SỞ',
    'Ngô Văn Sở',
]
OLD_PRINCIPAL = [
    'Phùng Thị Dung', 'Phùng Thị Dung', 'Phung Thi Dung'
]

r = requests.get(SOURCE, timeout=40, headers={'User-Agent':'Mozilla/5.0 (GitHub Actions sync)'})
r.raise_for_status()
r.encoding = r.apparent_encoding or r.encoding
page = r.text

soup = BeautifulSoup(page, 'html.parser')

# Thay nhận diện trong text, title/meta.
for node in soup.find_all(string=True):
    text = str(node)
    new = text
    for old in OLD_SCHOOL:
        new = new.replace(old, SCHOOL)
    for old in OLD_PRINCIPAL:
        new = new.replace(old, PRINCIPAL)
    if new != text:
        node.replace_with(new)

for tag in soup.find_all(['title','meta']):
    if tag.name == 'title' and tag.string:
        tag.string = str(tag.string).replace('Ngô Văn Sở', SCHOOL).replace('THCS Ngô Văn Sở', SCHOOL)
    if tag.name == 'meta' and tag.get('content'):
        c = tag['content']
        for old in OLD_SCHOOL: c = c.replace(old, SCHOOL)
        for old in OLD_PRINCIPAL: c = c.replace(old, PRINCIPAL)
        tag['content'] = c

# Làm asset URL tuyệt đối để chúng tiếp tục tải sau khi mirror.
for tag, attr in [('img','src'),('script','src'),('iframe','src'),('link','href'),('a','href')]:
    for el in soup.find_all(tag):
        val = el.get(attr)
        if not val or val.startswith(('#','javascript:','mailto:','tel:','data:','blob:')):
            continue
        el[attr] = urljoin(SOURCE, val)

# Không chạy JS của nguồn trong bản mirror.
for s in soup.find_all('script'):
    s.decompose()

# Khóa form để bản mirror không gửi dữ liệu đăng nhập.
for form in soup.find_all('form'):
    form['onsubmit'] = "return false;"
    form['action'] = '#'

# Tiêu đề/nhận diện an toàn.
head = soup.head
if head:
    meta = soup.new_tag('meta', attrs={'name':'robots','content':'noindex,nofollow'})
    head.append(meta)

body = soup.body or soup
banner = soup.new_tag('div')
banner['style'] = 'background:#0d3b66;color:#fff;padding:10px 16px;text-align:center;font:700 14px Arial;position:sticky;top:0;z-index:2147483647'
banner.string = 'TRƯỜNG THCS DƯƠNG MINH CHÂU — BẢN ĐỒNG BỘ KHÔNG CHÍNH THỨC'
body.insert(0, banner)

OUT.write_text(str(soup), encoding='utf-8')
print(f'Wrote {OUT} ({OUT.stat().st_size} bytes)')
