# CTF
new tools for studying while using ai tools help me get better score
# CTF Web Parser

一个用于 CTF Web 方向基础网页解析的 Python 小工具。

## 功能

- 获取网页并自动处理编码
- 提取标题、链接、表单、输入字段
- 提取 HTML 注释（常藏 flag / 提示）
- 扫描 `script` / `style` 中的可疑关键字
- 列出 `meta` 标签和资源引用

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```bash
python web_parser.py http://example.com
```

也可以将输出保存到文件：

```bash
python web_parser.py http://example.com > result.txt
```

## 输出内容

脚本会依次输出：

1. 状态码、页面大小、最终 URL
2. 页面标题
3. 所有链接
4. 表单及输入字段（包括隐藏字段）
5. HTML 注释
6. `script` / `style` 中的可疑字符串
7. `meta` 标签
8. 图片、脚本、CSS 等资源引用

## 免责声明

本工具仅用于 **授权测试、CTF 比赛、自己搭建的靶场** 等合法场景。  
请勿用于未授权的攻击或扫描行为。

## License

MIT
