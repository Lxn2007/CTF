#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Comment


def parse_webpage(url):
    """
    基础网页解析脚本
    功能：获取网页并提取标题、链接、表单、输入框、注释、脚本中的可疑信息
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)

        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding

        html = resp.text

        print(f"[+] 状态码: {resp.status_code}")
        print(f"[+] 页面大小: {len(html)} 字符")
        print(f"[+] 最终URL: {resp.url}")
        print("-" * 60)

        soup = BeautifulSoup(html, "html.parser")

        # 标题
        title = soup.title.string.strip() if soup.title and soup.title.string else "无标题"
        print(f"[标题] {title}")

        # 链接
        print("\n[链接]")
        links = set()
        for a in soup.find_all("a", href=True):
            full_url = urljoin(url, a["href"])
            links.add(full_url)
            print(f"  {a.get_text(strip=True)[:30]:30} -> {full_url}")
        if not links:
            print("  未发现链接")

        # 表单与输入字段
        print("\n[表单]")
        forms = soup.find_all("form")
        if not forms:
            print("  未发现表单")
        for i, form in enumerate(forms, 1):
            action = form.get("action", "")
            method = form.get("method", "get").upper()
            print(f"  表单 {i}: method={method}, action={urljoin(url, action)}")
            for inp in form.find_all(["input", "textarea", "select"]):
                name = inp.get("name", "无name")
                value = inp.get("value", "")
                typ = inp.get("type", inp.name)
                print(f"    - {typ:10} name={name:15} value={value}")

        # HTML 注释
        print("\n[注释]")
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        if not comments:
            print("  未发现注释")
        for c in comments:
            c = c.strip()
            if c:
                print(f"  <!-- {c} -->")

        # script / style 可疑字符串
        print("\n[脚本/样式中的可疑字符串]")
        suspicious_keywords = ["flag", "token", "secret", "key", "admin", "debug", "api"]
        found = False
        for tag in soup.find_all(["script", "style"]):
            content = tag.string if tag.string else ""
            for kw in suspicious_keywords:
                if kw.lower() in content.lower():
                    lines = content.splitlines()
                    for line in lines:
                        if kw.lower() in line.lower():
                            print(f"  [{tag.name}] {line.strip()[:120]}")
                            found = True
        if not found:
            print("  未发现明显可疑字符串")

        # Meta 标签
        print("\n[Meta 标签]")
        for meta in soup.find_all("meta"):
            attrs = {k: v for k, v in meta.attrs.items()}
            print(f"  {attrs}")

        # 资源引用
        print("\n[资源引用]")
        for tag, attr in [("img", "src"), ("script", "src"), ("link", "href")]:
            for item in soup.find_all(tag):
                src = item.get(attr)
                if src:
                    print(f"  {tag:6} -> {urljoin(url, src)}")

        print("\n[+] 解析完成")

    except requests.exceptions.RequestException as e:
        print(f"[-] 请求失败: {e}", file=sys.stderr)
    except Exception as e:
        print(f"[-] 解析出错: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="CTF Web 页面基础解析工具")
    parser.add_argument("url", help="目标 URL，例如 http://example.com")
    args = parser.parse_args()
    parse_webpage(args.url)


if __name__ == "__main__":
    main()
  #用目标网址替换name??
