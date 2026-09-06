#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urljoin
import re, requests
from bs4 import BeautifulSoup

SOURCES=[
 "https://thcsngovanso.phuonglaocai.edu.vn/",
 "http://thcsngovanso.phuonglaocai.edu.vn/",
 "https://ththcsngovanso.pgdlaocai.edu.vn/",
]
OUT=Path("synced.html")
SCHOOL="Trường THCS Dương Minh Châu"
PRINCIPAL="Nguyễn Xuân Phúc"
OLDSCHOOL=["Trường THCS Ngô Văn Sở","THCS Ngô Văn Sở","THCS NGÔ VĂN SỞ","Ngô Văn Sở"]
OLDPRINCIPAL=["Phùng Thị Dung","Phùng Thị Dung","Phung Thi Dung"]

def rewrite(page, base):
    soup=BeautifulSoup(page,"html.parser")
    for node in soup.find_all(string=True):
        t=str(node); n=t
        for x in OLDSCHOOL: n=n.replace(x,SCHOOL)
        for x in OLDPRINCIPAL: n=n.replace(x,PRINCIPAL)
        if n!=t: node.replace_with(n)
    if soup.title and soup.title.string:
        s=str(soup.title.string)
        for x in OLDSCHOOL: s=s.replace(x,SCHOOL)
        soup.title.string=s
    for tag in soup.find_all("meta"):
        if tag.get("content"):
            c=tag["content"]
            for x in OLDSCHOOL: c=c.replace(x,SCHOOL)
            for x in OLDPRINCIPAL: c=c.replace(x,PRINCIPAL)
            tag["content"]=c
    for tag,attr in [("img","src"),("link","href"),("a","href"),("iframe","src")]:
        for el in soup.find_all(tag):
            v=el.get(attr)
            if v and not v.startswith(("#","javascript:","mailto:","tel:","data:","blob:")):
                el[attr]=urljoin(base,v)
    for s in soup.find_all("script"): s.decompose()
    for form in soup.find_all("form"):
        form["action"]="#"; form["onsubmit"]="return false;"
    body=soup.body or soup
    banner=soup.new_tag("div")
    banner["style"]="background:#0d3b66;color:#fff;padding:10px 16px;text-align:center;font:700 14px Arial;position:sticky;top:0;z-index:2147483647"
    banner.string="TRƯỜNG THCS DƯƠNG MINH CHÂU — BẢN ĐỒNG BỘ KHÔNG CHÍNH THỨC"
    body.insert(0,banner)
    return "<!doctype html>\n"+str(soup)

last=None
for src in SOURCES:
    try:
        r=requests.get(src,timeout=30,headers={"User-Agent":"Mozilla/5.0 GitHub Actions"},allow_redirects=True)
        print(src, r.status_code, r.url, len(r.content))
        if r.ok and r.text.strip():
            OUT.write_text(rewrite(r.text,r.url),encoding="utf-8")
            print("SYNC_OK")
            raise SystemExit(0)
        last=f"HTTP {r.status_code}"
    except Exception as e:
        print("FAILED",src,e); last=str(e)
if OUT.exists() and OUT.stat().st_size>1000:
    print("SYNC_FAILED_BUT_KEEP_EXISTING",last)
    raise SystemExit(0)
print("NO_SOURCE_AVAILABLE",last)
raise SystemExit(1)
