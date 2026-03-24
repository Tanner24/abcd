import sys
import os
import re

dr = '/Users/yogiphil/Desktop/WEB DEVELOPMENT PROJECT/EXAMPLE1/pages/'
files = ['an-kinh-narthang.html', 'du-an-tu-vien.html', 'gay-quy-bao-tro.html', 'lich-su-narthang.html', 'thu-vien-hoc-thuat.html', 'truyen-thua-dao-su.html']

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

for fname in files:
    fpath = os.path.join(dr, fname)
    if not os.path.exists(fpath): continue
    
    with open(fpath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if "setLang" in content and ".nav-sticky" in content:
        continue
        
    start_pos = content.find('<div class="content-section">')
    if start_pos == -1:
        print(f"Skipping {fname}: no content-section")
        continue

    if "</style>" in content:
        content = content.replace("</style>", css_to_add + "\n    </style>")
        
    end_pos = content.find('</body>', start_pos)
    
    # Extract the block to wrap
    block = content[start_pos:end_pos]
    
    # These files don't have scripts, so we need to inject the script right before </body> or inside the block.
    # We will inject the script block right before </body>
    
    def make_block(lang):
        b = block
        return f'<div id="{lang}" class="lang-page{ " active-page" if lang == "vi" else "" }">\n{b}</div>\n'
        
    wrapped = nav_html + "\n" + make_block('vi') + make_block('en') + make_block('zh') + make_block('bo') + "\n<script>\n" + js_to_add + "\n</script>\n"
    
    content = content[:start_pos] + wrapped + content[end_pos:]
    
    with open(fpath, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Processed {fname}")

