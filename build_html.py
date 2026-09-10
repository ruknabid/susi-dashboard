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

    # 접수 마감일 태그 시각화 강화 (중복 치환 방지)
    html_content = re.sub(r'(?:<strong>)?9\.\s*10\(목\)\s*17:00(?:</strong>)?\s*🚨', '<span class="deadline-tag danger">9. 10(목) 17:00 🚨 (내일 마감)</span>', html_content)
    html_content = re.sub(r'(?:<strong>)?9\.\s*11\(금\)\s*17:00(?:</strong>)?\s*⚠️', '<span class="deadline-tag warning">9. 11(금) 17:00 ⚠️ (조기 마감)</span>', html_content)
    html_content = re.sub(r'9\.\s*11\(금\)\s*18:00', '<span class="deadline-tag normal">9. 11(금) 18:00</span>', html_content)

    template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2027 대학 입시 경쟁률 대시보드</title>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b0f19;
            --surface-color: rgba(22, 30, 49, 0.75);
            --text-main: #f8fafc;
            --accent: #3b82f6;
            --border-color: rgba(255, 255, 255, 0.12);
        }}
        body {{
            font-family: 'Pretendard', sans-serif;
            background-color: var(--bg-color);
            background-image: radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.18) 0px, transparent 50%),
                              radial-gradient(at 100% 100%, rgba(239, 68, 68, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            margin: 0; padding: 20px; line-height: 1.6;
        }}
        .container {{
            max-width: 1240px; margin: 0 auto; padding: 36px;
            background: var(--surface-color);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
        }}
        h1 {{ color: #fff; font-size: 2.3rem; font-weight: 800; background: linear-gradient(to right, #60a5fa, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 10px; margin-bottom: 20px; }}
        h2 {{ color: #fff; font-size: 1.5rem; border-bottom: 2px solid var(--border-color); padding-bottom: 10px; margin-top: 40px; }}
        h3 {{ color: #93c5fd; font-size: 1.2rem; margin-top: 25px; }}
        table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 20px 0; border-radius: 12px; overflow: hidden; border: 1px solid var(--border-color); }}
        th, td {{ padding: 14px 16px; text-align: left; border-bottom: 1px solid rgba(255, 255, 255, 0.07); background: rgba(17, 24, 39, 0.5); font-size: 0.95rem; }}
        th {{ background: rgba(15, 23, 42, 0.9); font-weight: 700; color: #cbd5e1; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.05em; }}
        tr:hover td {{ background: rgba(30, 41, 59, 0.7); }}
        a {{ color: #60a5fa; text-decoration: none; font-weight: 500; }}
        a:hover {{ color: #93c5fd; text-decoration: underline; }}
        blockquote {{ margin: 20px 0; padding: 20px 24px; border-left: 4px solid var(--accent); background: rgba(59, 130, 246, 0.1); border-radius: 0 12px 12px 0; }}

        /* 긴급 마감 배너 카드 */
        .deadline-alert-banner {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(245, 158, 11, 0.15));
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 28px;
            box-shadow: 0 10px 25px -5px rgba(239, 68, 68, 0.2);
        }}
        .deadline-alert-title {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.15rem;
            font-weight: 800;
            color: #fca5a5;
            margin-bottom: 14px;
        }}
        .deadline-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 12px;
        }}
        .deadline-card {{
            background: rgba(15, 23, 42, 0.75);
            padding: 14px 18px;
            border-radius: 12px;
            border-left: 5px solid #64748b;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .deadline-card.urgent {{
            border-left-color: #ef4444;
            background: rgba(239, 68, 68, 0.12);
        }}
        .deadline-card.warning {{
            border-left-color: #f59e0b;
            background: rgba(245, 158, 11, 0.12);
        }}
        .deadline-card.normal {{
            border-left-color: #3b82f6;
            background: rgba(59, 130, 246, 0.1);
        }}
        .deadline-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .deadline-card .univ {{
            font-weight: 700;
            font-size: 1rem;
            color: #fff;
        }}
        .deadline-card .dday {{
            font-size: 0.75rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 9999px;
        }}
        .deadline-card.urgent .dday {{ background: #ef4444; color: #fff; animation: pulse 1.8s infinite; }}
        .deadline-card.warning .dday {{ background: #f59e0b; color: #000; }}
        .deadline-card.normal .dday {{ background: #334155; color: #cbd5e1; }}
        .deadline-card .time {{
            font-size: 0.92rem;
            color: #e2e8f0;
            font-weight: 600;
        }}
        .deadline-card .desc {{
            font-size: 0.8rem;
            color: #94a3b8;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.85; transform: scale(1.03); }}
        }}

        /* 표 내부 마감일 뱃지 */
        .deadline-tag {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 700;
            white-space: nowrap;
        }}
        .deadline-tag.danger {{
            background: rgba(239, 68, 68, 0.25);
            color: #fca5a5;
            border: 1px solid #ef4444;
        }}
        .deadline-tag.warning {{
            background: rgba(245, 158, 11, 0.25);
            color: #fcd34d;
            border: 1px solid #f59e0b;
        }}
        .deadline-tag.normal {{
            background: rgba(59, 130, 246, 0.2);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.4);
        }}

        @media (max-width: 768px) {{
            .container {{ padding: 18px; border-radius: 16px; }}
            table {{ display: block; overflow-x: auto; white-space: nowrap; }}
            h1 {{ font-size: 1.8rem; }}
        }}
        .header-actions {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            background: rgba(15, 23, 42, 0.6);
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
                <span>⏱️ 경쟁률 최종 갱신:</span>
                <strong>{last_updated}</strong>
            </div>
            <a href="https://github.com/ruknabid/susi-dashboard/actions/workflows/update.yml" target="_blank" class="refresh-btn">
                🔄 강제 실시간 갱신 (스위치 켜기)
            </a>
        </div>

        <!-- 긴급 마감일 안내 배너 -->
        <div class="deadline-alert-banner">
            <div class="deadline-alert-title">
                <span>🚨 2027 수시 원서접수 마감 시한 핵심 체크</span>
            </div>
            <div class="deadline-grid">
                <div class="deadline-card normal">
                    <div class="deadline-card-header">
                        <span class="univ">이화여자대학교</span>
                        <span class="dday" style="background:#64748b;">접수 마감 완료</span>
                    </div>
                    <div class="time">9월 10일(목) 17:00 마감</div>
                    <div class="desc">✅ 접수 종료 (사회복지 51.17:1, 인문I 전체 57.95:1 최종 마감)</div>
                </div>
                <div class="deadline-card urgent">
                    <div class="deadline-card-header">
                        <span class="univ">한국외국어대학교</span>
                        <span class="dday">내일 조기마감! ⚠️</span>
                    </div>
                    <div class="time">9월 11일(금) 17:00 마감</div>
                    <div class="desc">🚨 18시가 아닌 17시 마감! 내일 오후 3시 이전 결제 완료 필수</div>
                </div>
                <div class="deadline-card warning">
                    <div class="deadline-card-header">
                        <span class="univ">기타 8개 대학</span>
                        <span class="dday">내일 최종마감 ⏳</span>
                    </div>
                    <div class="time">9월 11일(금) 18:00 마감</div>
                    <div class="desc">중앙, 경희, 성균관, 숭실, 세종, 서울여, 덕성여, 가천대 (오후 3~4시 결제 권장)</div>
                </div>
            </div>
        </div>

        <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 25px; text-align: right;">
            * 버튼 클릭 후 <strong>Run workflow</strong>를 누르시면 30초 뒤 전체 데이터가 자동 갱신됩니다.
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
