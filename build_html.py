import os
import markdown
import re

def build():
    with open('경쟁률_현황.md', 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 마지막 업데이트 시간 파싱
    match = re.search(r'\((.* 현황 업데이트)\)', md_text)
    last_updated = match.group(1) if match else '업데이트 시간 알 수 없음'

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
        .header-actions {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            background: rgba(15, 23, 42, 0.5);
            padding: 15px 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            flex-wrap: wrap;
            gap: 15px;
        }}
        .update-time {{
            color: #94a3b8;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .update-time strong {{
            color: #34d399;
            font-weight: 600;
        }}
        .refresh-btn {{
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.4);
        }}
        .refresh-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px -2px rgba(59, 130, 246, 0.6);
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-actions">
            <div class="update-time">
                <span>⏱️ 마지막 갱신:</span>
                <strong>{last_updated}</strong>
            </div>
            <a href="https://github.com/ruknabid/susi-dashboard/actions/workflows/update.yml" target="_blank" class="refresh-btn">
                🔄 강제 실시간 갱신 (스위치 켜기)
            </a>
        </div>
        <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 30px; text-align: right;">
            * 버튼 클릭 후 <strong>Run workflow</strong> 버튼을 누르시면 30초 뒤 표가 갱신됩니다.
        </div>
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
