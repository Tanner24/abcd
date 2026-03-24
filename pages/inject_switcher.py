import sys
import os
import re

dr = '/Users/yogiphil/Desktop/WEB DEVELOPMENT PROJECT/EXAMPLE1/pages/'
files = []
try:
    files = [f for f in os.listdir(dr) if f.endswith('.html') and f != '84-mahasiddhas.html']
except Exception as e:
    print(f"Error reading dir: {e}")
    sys.exit(1)

css_to_add = """
        .nav-sticky {
            position: sticky;
            top: 0;
            background: rgba(139, 0, 0, 0.9);
            padding: 15px;
            display: flex;
            justify-content: center;
            gap: 15px;
            z-index: 1000;
            border-bottom: 2px solid var(--wisdom-gold);
            backdrop-filter: blur(10px);
        }

        .flag-btn {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid var(--narthang-gold);
            cursor: pointer;
            transition: 0.3s;
            border-radius: 4px;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            font-weight: 600;
            color: var(--lotus-white, #fdf5e6);
            font-family: 'Montserrat', sans-serif;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
        }

        .flag-btn:hover,
        .flag-btn.active-btn {
            background: var(--wisdom-gold, #c5a059);
            color: #000;
            box-shadow: 0 0 15px var(--wisdom-gold, #c5a059);
            transform: translateY(-2px);
        }

        .flag-btn img {
            width: 20px;
            height: 14px;
            margin-right: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .lang-page {
            display: none;
            width: 100%;
        }

        .lang-page.active-page {
            display: contents;
        }

        @media (max-width: 768px) {
            .nav-sticky {
                flex-wrap: wrap;
                gap: 10px;
            }
            .flag-btn {
                padding: 6px 12px;
                font-size: 0.7rem;
            }
        }
"""

nav_html = """
    <div class="nav-sticky">
        <button class="flag-btn" id="btn-vi" onclick="setLang('vi')">
            <img src="https://flagcdn.com/w80/vn.png" alt="VN"> TIẾNG VIỆT
        </button>
        <button class="flag-btn" id="btn-en" onclick="setLang('en')">
            <img src="https://flagcdn.com/w80/us.png" alt="EN"> ENGLISH
        </button>
        <button class="flag-btn" id="btn-zh" onclick="setLang('zh')">
            <img src="https://flagcdn.com/w80/cn.png" alt="CN"> 中文
        </button>
        <button class="flag-btn" id="btn-bo" onclick="setLang('bo')">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Flag_of_Tibet.svg/1920px-Flag_of_Tibet.svg.png"
                alt="BO"> བོད་སྐད།
        </button>
    </div>
"""

js_to_add = """
        function setLang(langId) {
            localStorage.setItem('selectedLanguage', langId);
            document.querySelectorAll('.lang-page').forEach(p => p.classList.remove('active-page'));
            const targetPage = document.getElementById(langId);
            if (targetPage) targetPage.classList.add('active-page');
            document.querySelectorAll('.flag-btn').forEach(btn => btn.classList.remove('active-btn'));
            const activeBtn = document.getElementById('btn-' + langId);
            if (activeBtn) activeBtn.classList.add('active-btn');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        window.addEventListener('DOMContentLoaded', () => {
            const savedLang = localStorage.getItem('selectedLanguage') || 'vi';
            setLang(savedLang);
        });
"""

print(f"Total files: {len(files)}")
for fname in files:
    fpath = os.path.join(dr, fname)
    try:
        with open(fpath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if "setLang" in content and ".nav-sticky" in content:
            print(f"Skipping {fname}: already has switcher")
            continue # already has it
            
        # ADD CSS
        if "</style>" in content:
            content = content.replace("</style>", css_to_add + "\n    </style>")
        else:
            print(f"Warning: no </style> in {fname}")

        # ADD JS
        if "<script>" in content:
            content = content.replace("<script>", "<script>\n" + js_to_add, 1)
        elif "<script src" in content:
            # insert before first script
            content = re.sub(r'(<script src="[^"]+"></script>)', r'<script>\n' + js_to_add + '\n</script>\n\n    \g<1>', content, count=1)
        else:
            print(f"Warning: no <script> in {fname}")
        
        # FIND CONTENT BLOCK START
        start_pos = -1
        markers = ['    <div class="main-wrapper">', '    <div class="container"', '    <div class="wiki-container"', '    <div class="portal-container"']
        for marker in markers:
            pos = content.find(marker)
            if pos != -1 and (start_pos == -1 or pos < start_pos):
                start_pos = pos

        if start_pos == -1:
            # fallback: find first <main
            pos = content.find('<main')
            if pos != -1: start_pos = pos
            else:
                print(f"Skipping {fname}: could not find main content marker.")
                continue
                
        # FIND CONTENT BLOCK END (usually before the first script tag)
        end_pos = content.find('<script', start_pos)
        if end_pos == -1: end_pos = content.find('</body>', start_pos)
        if end_pos == -1: end_pos = len(content)
        
        # Extract the block to wrap
        block = content[start_pos:end_pos]
        
        # duplicate block for each lang and modify ids to prevent conflict
        def make_block(lang):
            b = block
            if 'id="main-container"' in b:
                b = b.replace('id="main-container"', f'id="main-container-{lang}"')
            return f'<div id="{lang}" class="lang-page{ " active-page" if lang == "vi" else "" }">\n{b}</div>\n'
            
        wrapped = nav_html + "\n" + make_block('vi') + make_block('en') + make_block('zh') + make_block('bo')
        
        content = content[:start_pos] + wrapped + content[end_pos:]
        
        with open(fpath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Processed {fname}")
    except Exception as e:
        print(f"Error processing {fname}: {e}")

