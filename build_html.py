import os
import markdown

def build():
    with open('경쟁률_현황.md', 'r', encoding='utf-8') as f:
        md_text = f.read()

    html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

    template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2027 대학 입시 경쟁률 대시보드</title>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --surface-color: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --accent: #3b82f6;
            --border-color: rgba(255, 255, 255, 0.1);
        }}
        body {{
            font-family: 'Pretendard', sans-serif;
            background-color: var(--bg-color);
            background-image: radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                              radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            margin: 0; padding: 20px; line-height: 1.6;
        }}
        .container {{
            max-width: 1200px; margin: 0 auto; padding: 40px;
            background: var(--surface-color);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
        }}
        h1 {{ color: #fff; font-size: 2.5rem; background: linear-gradient(to right, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        h2, h3 {{ color: #fff; }}
        h2 {{ border-bottom: 2px solid var(--border-color); padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 25px 0; border-radius: 12px; overflow: hidden; }}
        th, td {{ padding: 16px 20px; text-align: left; border-bottom: 1px solid var(--border-color); background: rgba(30, 41, 59, 0.4); }}
        th {{ background: rgba(15, 23, 42, 0.8); font-weight: 600; color: #cbd5e1; text-transform: uppercase; font-size: 0.85rem; }}
        tr:hover td {{ background: rgba(51, 65, 85, 0.6); }}
        a {{ color: #60a5fa; text-decoration: none; }}
        a:hover {{ color: #93c5fd; }}
        blockquote {{ margin: 20px 0; padding: 20px 24px; border-left: 4px solid var(--accent); background: rgba(59, 130, 246, 0.1); border-radius: 0 12px 12px 0; }}
        @media (max-width: 768px) {{
            .container {{ padding: 20px; border-radius: 16px; }}
            table {{ display: block; overflow-x: auto; white-space: nowrap; }}
            h1 {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(template)
    print("index.html 생성 완료!")

if __name__ == "__main__":
    build()
