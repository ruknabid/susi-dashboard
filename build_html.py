import os
import markdown
import re
from datetime import datetime, timezone, timedelta

def build():
    with open('경쟁률_현황.md', 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 마지막 업데이트 시간 파싱
    KST = timezone(timedelta(hours=9))
    now_dt = datetime.now(KST)
    full_now_str = now_dt.strftime('%Y년 %m월 %d일 %H:%M')

    match = re.search(r'\((.* 현황 업데이트)\)', md_text)
    last_updated = match.group(1) if match else f'{full_now_str} (KST)'

    html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

    # 접수 마감일 태그 시각화 강화
    html_content = re.sub(r'(?:<strong>)?9\.\s*11\(금\)\s*17:00(?:</strong>)?\s*⚠️', '<span class="deadline-tag danger">9. 11(금) 17:00 ⚠️ (마감 종료)</span>', html_content)
    html_content = re.sub(r'9\.\s*11\(금\)\s*18:00', '<span class="deadline-tag warning">9. 11(금) 18:00 (마감 임박)</span>', html_content)

    # 접수 상태 뱃지 시각화
    html_content = re.sub(r'(?:<strong>)?✅\s*접수/결제\s*완료(?:</strong>)?', '<span class="status-badge paid">✅ 결제 완료</span>', html_content)
    html_content = re.sub(r'\[\s*\]\s*미결제\s*\(교체\s*검토\)', '<span class="status-badge review">⚠️ 교체 검토</span>', html_content)
    html_content = re.sub(r'\[\s*\]\s*미결제\s*\(검토\s*중\)', '<span class="status-badge pending">⏳ 검토 중</span>', html_content)
    html_content = re.sub(r'\[\s*\]\s*예비\s*검토', '<span class="status-badge backup">예비 검토</span>', html_content)

    template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2027 송연 수시 6장 최종 접수 현황 & 경쟁률 대시보드</title>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #080c14;
            --surface-color: rgba(18, 26, 43, 0.82);
            --text-main: #f8fafc;
            --accent: #3b82f6;
            --emerald: #10b981;
            --border-color: rgba(255, 255, 255, 0.12);
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Pretendard', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.18) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(59, 130, 246, 0.20) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 60%);
            background-attachment: fixed;
            color: var(--text-main);
            margin: 0; padding: 24px 16px; line-height: 1.65;
        }}
        .container {{
            max-width: 1280px; margin: 0 auto; padding: 40px;
            background: var(--surface-color);
            backdrop-filter: blur(24px);
            border: 1px solid var(--border-color);
            border-radius: 28px;
            box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.65);
        }}
        h1 {{ 
            font-size: 2.35rem; font-weight: 900; letter-spacing: -0.03em;
            background: linear-gradient(135deg, #34d399 0%, #60a5fa 50%, #c084fc 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-top: 10px; margin-bottom: 24px;
        }}
        h2 {{ color: #fff; font-size: 1.55rem; border-bottom: 2px solid var(--border-color); padding-bottom: 12px; margin-top: 48px; }}
        h3 {{ color: #93c5fd; font-size: 1.25rem; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 24px 0; border-radius: 14px; overflow: hidden; border: 1px solid var(--border-color); }}
        th, td {{ padding: 15px 18px; text-align: left; border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: rgba(15, 23, 42, 0.55); font-size: 0.95rem; }}
        th {{ background: rgba(15, 23, 42, 0.95); font-weight: 700; color: #cbd5e1; text-transform: uppercase; font-size: 0.86rem; letter-spacing: 0.05em; }}
        tr:hover td {{ background: rgba(30, 41, 59, 0.75); }}
        a {{ color: #60a5fa; text-decoration: none; font-weight: 500; }}
        a:hover {{ color: #93c5fd; text-decoration: underline; }}
        blockquote {{ margin: 24px 0; padding: 22px 28px; border-left: 4px solid var(--accent); background: rgba(59, 130, 246, 0.12); border-radius: 0 14px 14px 0; }}

        /* 100% 완료 축하 배너 */
        .celebration-banner {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.22), rgba(59, 130, 246, 0.22));
            border: 2px solid rgba(52, 211, 153, 0.6);
            border-radius: 20px;
            padding: 24px 28px;
            margin-bottom: 28px;
            box-shadow: 0 15px 35px -5px rgba(16, 185, 129, 0.35);
            animation: glow 3s infinite alternate;
        }}
        @keyframes glow {{
            0% {{ box-shadow: 0 10px 30px -5px rgba(16, 185, 129, 0.3); }}
            100% {{ box-shadow: 0 15px 45px 0px rgba(52, 211, 153, 0.5); }}
        }}
        .celebration-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 16px;
        }}
        .celebration-title {{
            font-size: 1.35rem;
            font-weight: 900;
            color: #34d399;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .celebration-badge {{
            font-size: 0.9rem;
            font-weight: 800;
            background: rgba(16, 185, 129, 0.3);
            color: #34d399;
            padding: 6px 16px;
            border-radius: 9999px;
            border: 1px solid rgba(52, 211, 153, 0.7);
        }}
        .progress-bar-bg {{
            background: rgba(15, 23, 42, 0.85);
            border-radius: 9999px;
            height: 12px;
            overflow: hidden;
            margin-bottom: 18px;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }}
        .progress-bar-fill {{
            background: linear-gradient(90deg, #10b981, #06b6d4, #3b82f6);
            height: 100%;
            width: 100%;
            border-radius: 9999px;
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.8);
        }}
        .final-cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 14px;
        }}
        .final-card {{
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(52, 211, 153, 0.3);
            border-radius: 12px;
            padding: 14px 18px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .final-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(52, 211, 153, 0.7);
        }}
        .final-card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .final-card .univ-name {{
            font-size: 1.05rem;
            font-weight: 800;
            color: #fff;
        }}
        .final-card .app-no {{
            font-family: monospace;
            font-size: 0.85rem;
            background: rgba(59, 130, 246, 0.2);
            color: #93c5fd;
            padding: 2px 8px;
            border-radius: 6px;
            border: 1px solid rgba(59, 130, 246, 0.4);
        }}
        .final-card .dept-info {{
            font-size: 0.92rem;
            color: #cbd5e1;
            font-weight: 500;
        }}
        .final-card .meta-info {{
            display: flex;
            justify-content: space-between;
            font-size: 0.82rem;
            color: #94a3b8;
            margin-top: 4px;
            padding-top: 6px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }}

        /* 상태 뱃지 */
        .status-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 800;
            white-space: nowrap;
        }}
        .status-badge.paid {{
            background: rgba(16, 185, 129, 0.22);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.6);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.25);
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

        /* 접수증 이미지 섹션 */
        .receipt-section {{
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin: 32px 0;
        }}
        .receipt-title {{
            font-size: 1.15rem;
            font-weight: 800;
            color: #93c5fd;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .receipt-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }}
        .receipt-card {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
            text-align: center;
        }}
        .receipt-card img {{
            width: 100%;
            height: auto;
            display: block;
            cursor: pointer;
            transition: transform 0.3s ease;
        }}
        .receipt-card img:hover {{
            transform: scale(1.02);
        }}
        .receipt-label {{
            padding: 10px;
            font-size: 0.88rem;
            font-weight: 600;
            color: #cbd5e1;
            background: rgba(15, 23, 42, 0.8);
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            background: rgba(15, 23, 42, 0.6);
            padding: 16px 24px;
            border-radius: 14px;
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
            font-weight: 700;
        }}
        .refresh-btn {{
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 8px -1px rgba(59, 130, 246, 0.4);
        }}
        .refresh-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 14px -2px rgba(59, 130, 246, 0.6);
            color: white;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 20px 16px; border-radius: 18px; }}
            table {{ display: block; overflow-x: auto; white-space: nowrap; }}
            h1 {{ font-size: 1.85rem; }}
            .final-cards-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-actions">
            <div class="update-time">
                <span>⏱️ 최종 확인 시각:</span>
                <strong>{last_updated}</strong>
            </div>
            <a href="https://github.com/ruknabid/susi-dashboard/actions/workflows/update.yml" target="_blank" class="refresh-btn">
                🔄 원클릭 실시간 갱신 (GitHub Actions)
            </a>
        </div>

        <!-- 🎯 6장 100% 결제 완료 축하 배너 -->
        <div class="celebration-banner">
            <div class="celebration-header">
                <span class="celebration-title">🎉 2027 송연 수시 6장 원서 접수 및 결제 100% 최종 완료!</span>
                <span class="celebration-badge">6 / 6장 완료 (결제 총액: 420,000원)</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill"></div>
            </div>
            <div class="final-cards-grid">
                <div class="final-card">
                    <div class="final-card-top">
                        <span class="univ-name">숭실대학교</span>
                        <span class="app-no">수험: 121460163</span>
                    </div>
                    <div class="dept-info">SSU미래인재(학종) · 평생교육학과 (9명)</div>
                    <div class="meta-info">
                        <span>경쟁률: <strong>18.89 : 1 [최종]</strong></span>
                        <span>면접: 11. 27(금)</span>
                        <span style="color:#34d399; font-weight:700;">85,000원 결제</span>
                    </div>
                </div>

                <div class="final-card">
                    <div class="final-card-top">
                        <span class="univ-name">서울여자대학교</span>
                        <span class="app-no">수험: 34260124</span>
                    </div>
                    <div class="dept-info">바롬인재면접(학종) · 행정학과 (8명)</div>
                    <div class="meta-info">
                        <span>경쟁률: <strong>12.13 : 1</strong></span>
                        <span>면접: 11. 28(토)</span>
                        <span style="color:#34d399; font-weight:700;">70,000원 결제</span>
                    </div>
                </div>

                <div class="final-card">
                    <div class="final-card-top">
                        <span class="univ-name">덕성여자대학교</span>
                        <span class="app-no">수험: 1051N1246</span>
                    </div>
                    <div class="dept-info">덕성인재Ⅱ(학종) · 글로벌융합대학(인문사회 74명)</div>
                    <div class="meta-info">
                        <span>경쟁률: <strong>16.11 : 1</strong></span>
                        <span>면접: 11. 22(일)</span>
                        <span style="color:#34d399; font-weight:700;">75,000원 결제</span>
                    </div>
                </div>

                <div class="final-card">
                    <div class="final-card-top">
                        <span class="univ-name">가천대학교</span>
                        <span class="app-no">수험: 2197402578</span>
                    </div>
                    <div class="dept-info">지역균형(교과면접) · 자유전공학부 (321명)</div>
                    <div class="meta-info">
                        <span>경쟁률: <strong>12.50 : 1</strong></span>
                        <span>면접: 12. 5~7</span>
                        <span style="color:#34d399; font-weight:700;">65,000원 결제</span>
                    </div>
                </div>

                <div class="final-card">
                    <div class="final-card-top">
                        <span class="univ-name">경희대학교(국제)</span>
                        <span class="app-no">수험: 3275010016</span>
                    </div>
                    <div class="dept-info">지역균형(교과) · 프랑스어학과 (3명) 🎯</div>
                    <div class="meta-info">
                        <span>경쟁률: <strong>2.67 : 1 (초저)</strong></span>
                        <span>수능최저: 2합5</span>
                        <span style="color:#34d399; font-weight:700;">65,000원 결제</span>
                    </div>
                </div>

                <div class="final-card">
                    <div class="final-card-top">
                        <span class="univ-name">한국외국어대학교</span>
                        <span class="app-no">수험: 261500192</span>
                    </div>
                    <div class="dept-info">논술전형 · 인도·남아시아학과 (4명)</div>
                    <div class="meta-info">
                        <span>경쟁률: <strong>59.25 : 1 [최종]</strong></span>
                        <span>논술: 11. 29(일)</span>
                        <span style="color:#34d399; font-weight:700;">60,000원 결제</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 📷 원서 접수증 확인 섹션 -->
        <div class="receipt-section">
            <div class="receipt-title">
                <span>📄 최종 원서 접수증 확인 (유웨이어플라이 & 진학어플라이)</span>
            </div>
            <div class="receipt-grid">
                <div class="receipt-card">
                    <a href="송연수시접수_1.JPG" target="_blank">
                        <img src="송연수시접수_1.JPG" alt="송연 수시 접수증 1" loading="lazy">
                    </a>
                    <div class="receipt-label">📌 진학어플라이 / 유웨이어플라이 접수 내역 1 (클릭 시 원본 확대)</div>
                </div>
                <div class="receipt-card">
                    <a href="송연수시접수_2.JPG" target="_blank">
                        <img src="송연수시접수_2.JPG" alt="송연 수시 접수증 2" loading="lazy">
                    </a>
                    <div class="receipt-label">📌 진학어플라이 / 유웨이어플라이 접수 내역 2 (클릭 시 원본 확대)</div>
                </div>
            </div>
        </div>

        {html_content}
    </div>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(template)
    print("index.html 최종 빌드 완료!")

if __name__ == "__main__":
    build()
