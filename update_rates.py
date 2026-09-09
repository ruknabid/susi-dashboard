import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import re

headers = {'User-Agent': 'Mozilla/5.0'}

def get_html(url, encoding):
    req = urllib.request.Request(url, headers=headers)
    try:
        return urllib.request.urlopen(req, timeout=10).read().decode(encoding, errors='replace')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ''

targets = [
    ('중앙대학교', '성장형인재', '공공인재학부', 'https://ratio.uwayapply.com/Sl5KOjhMSmYlJjomSjdmVGY=', 'euc-kr'),
    ('세종대학교', '지역균형', '자유전공', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10950721.html', 'utf-8'),
    ('가천대학교', '학생부우수자', '심리학과', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10190711.html', 'utf-8'),
    ('가천대학교', '지역균형', '자유전공', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10190711.html', 'utf-8'),
    ('숭실대학교', 'SSU미래인재전형-면접형', '사회복지학부', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio11010851.html', 'utf-8'),
    ('한국외국어대학교', '논술', '베트남학과', 'https://ratio.uwayapply.com/Sl5KJmg6fEpmJSY6Jko3ZlRm', 'euc-kr'),
    ('한국외국어대학교', '논술', '인도·남아시아', 'https://ratio.uwayapply.com/Sl5KJmg6fEpmJSY6Jko3ZlRm', 'euc-kr'),
    ('이화여자대학교', '논술', '인문Ⅰ', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio11202121.html', 'utf-8'),
    ('덕성여자대학교', '덕성인재전형Ⅱ', '글로벌융합대학(인문사회)', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10530631.html', 'utf-8'),
    ('서울여자대학교', '바롬인재면접', '사회복지', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10860821.html', 'utf-8'),
    ('서울여자대학교', '교과우수자전형', '사회복지', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10860821.html', 'utf-8'),
    ('서울여자대학교', '교과우수자전형', '행정', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10860821.html', 'utf-8'),
    ('경희대학교', '지역균형', '프랑스어', 'https://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSjdmVGY=', 'euc-kr'),
    ('경희대학교', '논술우수자전형', '프랑스어', 'https://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSjdmVGY=', 'euc-kr'),
    ('경희대학교', '논술우수자전형', '러시아어', 'https://ratio.uwayapply.com/Sl5KOnw5SmYlJjomSjdmVGY=', 'euc-kr'),
    ('한국외국어대학교', '논술', '일본언어문화', 'https://ratio.uwayapply.com/Sl5KJmg6fEpmJSY6Jko3ZlRm', 'euc-kr'),
    ('한국외국어대학교', '논술', '이탈리아어과', 'https://ratio.uwayapply.com/Sl5KJmg6fEpmJSY6Jko3ZlRm', 'euc-kr'),
    ('숭실대학교', 'SSU미래인재전형-면접형', '평생교육', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio11010851.html', 'utf-8'),
    ('숭실대학교', 'SSU미래인재전형-면접형', '정치외교', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio11010851.html', 'utf-8'),
    ('세종대학교', '세종인재(면접형)', '행정', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10950721.html', 'utf-8'),
    ('세종대학교', '세종인재(면접형)', '법학', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10950721.html', 'utf-8'),
    ('가천대학교', '학생부우수자', '사회복지학과', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10190711.html', 'utf-8'),
    ('가천대학교', '학생부우수자', '법과대학', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10190711.html', 'utf-8'),
    ('성균관대학교', '융합인재', '인문과학계열', 'https://addon.jinhakapply.com/RatioV1/RatioH/Ratio10920591.html', 'utf-8')
]

def update_markdown(updates):
    md_path = '경쟁률_현황.md'
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return
        
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.strip().startswith('|') and '대학명' not in line and ':---' not in line:
            cells = [c.strip() for c in line.split('|')]
            if len(cells) > 6:
                univ = cells[1].replace('**', '').strip()
                track = cells[2].replace('**', '').strip()
                dept = cells[3].replace('**', '').strip()
                
                for (u, t, d), (quota, app, ratio) in updates.items():
                    if u in univ:
                        if d in dept or dept in d:
                            t_norm = re.sub(r'[^\w]', '', t)
                            track_norm = re.sub(r'[^\w]', '', track)
                            if (t_norm in track_norm or track_norm in t_norm or
                                ('교과' in t_norm and '교과' in track_norm) or
                                ('바롬' in t_norm and '바롬' in track_norm) or
                                ('논술' in t_norm and '논술' in track_norm)):
                                cells[4] = quota
                                cells[5] = app
                                cells[6] = ratio
                                line = ' | '.join(cells)
                                break
        new_lines.append(line)
        
    # Update timestamp in the header (KST 적용)
    KST = timezone(timedelta(hours=9))
    now_str = datetime.now(KST).strftime('%m월 %d일 %H:%M')
    for i, line in enumerate(new_lines):
        if '3. 대학별 경쟁률 요약' in line:
            new_lines[i] = f"## 3. 대학별 경쟁률 요약 ({now_str} 현황 업데이트)"

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

def main():
    KST = timezone(timedelta(hours=9))
    print(f"\n[{datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}] 실시간 경쟁률 업데이트 시작...\n")
    cache = {}
    updates = {}
    
    for univ, track, dept, url, enc in targets:
        if url not in cache:
            cache[url] = BeautifulSoup(get_html(url, enc), 'html.parser')
        
        soup = cache[url]
        found = False
        
        for t in soup.find_all('table'):
            ctx = ''
            prev_h2 = t.find_previous_sibling('h2')
            if prev_h2: ctx += prev_h2.text.strip()
            prev_div = t.find_previous_sibling('div')
            if prev_div: ctx += prev_div.text.strip()
            
            rows = t.find_all('tr')
            if rows:
                first_row = [c.text.strip() for c in rows[0].find_all(['th','td'])]
                ctx += ' ' + ' '.join(first_row)
            
            if track.replace(' ', '') not in ctx.replace(' ', ''):
                continue
                
            for r in rows:
                cells = [c.text.strip().replace('\n', '').replace('\r', '') for c in r.find_all(['th','td'])]
                if len(cells) >= 4 and any(dept in c for c in cells):
                    ratio = cells[-1]
                    app = cells[-2]
                    quota = cells[-3]
                    
                    updates[(univ, track, dept)] = (quota + "명", app + "명", ratio)
                    found = True
                    break
            
            if found:
                break
                
    update_markdown(updates)
    print("경쟁률 업데이트 및 마크다운 수정 완료!")

if __name__ == "__main__":
    main()
