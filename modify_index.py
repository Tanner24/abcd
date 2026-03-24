import re

with open('/Users/yogiphil/Desktop/WEB DEVELOPMENT PROJECT/EXAMPLE1/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the body parts
# The parts to duplicate are from `    <div class="container" id="main-container">`
# down to `    </div>` (the footage container)

match = re.search(r'(    <div class="container" id="main-container">.*?)(    <!-- FOOTAGE SECTION: PROJECT, HISTORY, RESOURCES -->.*?    </div>\n)', content, re.DOTALL)
if not match:
    print("Could not find containers!")
    exit(1)

main_container = match.group(1)
footage_container = match.group(2)

original_blocks = main_container + "\n" + footage_container

# We'll write a wrapper:
# <div id="vi" class="lang-page active-page">
#   ...
# </div>
# <div id="en" class="lang-page">
#   ...
# </div> ...

def translate_block(text, lang):
    # This is a naive replacement using a dictionary.
    
    # Dictionary of replacements
    replacements = {
        'en': {
            'OLD KADAMPA VN': 'OLD KADAMPA VN',
            'NARTHANG KADAMPA': 'NARTHANG KADAMPA',
            'Hoá thân thành tựu sự nghiệp của Đại Thành Tựu Giả Tumton Lodro Drakpa — Người sáng lập tu viện Narthang Gompa.': 'The emanation of Mahasiddha Tumton Lodro Drakpa — Founder of Narthang Gompa monastery.',
            'Đại Luận Sư Atisha — Người phục hưng Phật Pháp tại Tây Tạng, khai sáng dòng truyền thừa Kadampa.': 'The Great Master Atisha — Restorer of Buddhism in Tibet, founder of the Kadampa lineage.',
            'Đại Thành Tựu Giả Tumton Lodro Drakpa — Người sáng lập tu viện Narthang Gompa huyền thoại.': 'Mahasiddha Tumton Lodro Drakpa — Founder of the legendary Narthang Gompa monastery.',
            'Đức Phật Thích Ca Mâu Ni — Bậc Đạo Sư gốc của cõi Ta Bà, người khai sáng đạo Phật.': 'Shakyamuni Buddha — The root Guru of the Saha world, founder of Buddhism.',
            'Đức Quán Thế Âm — Lòng từ bi bao trùm khắp tam giới.': 'Avalokitesvara — Compassion encompassing the three realms.',
            'Đức Văn Thù Sư Lợi — Trí tuệ tỏa sáng xua tan màn vô minh.': 'Manjushri — Radiant wisdom dispelling the darkness of ignorance.',
            'Lục Độ Phật Mẫu Tara — Sinh ra từ giọt nước mắt bi mẫn của Đức Quán Thế Âm.': 'Green Tara — Born from the compassionate tears of Avalokitesvara.',
            'Bạch Độ Phật Mẫu — Hiện thân của trường thọ, trí tuệ và sự bình an vô biên.': 'White Tara — Embodiment of longevity, wisdom, and boundless peace.',
            'Dược Sư Lưu Ly Quang Vương Phật — Tiêu trừ bệnh tật, ban phước trường thọ.': 'Medicine Buddha — Dispelling illness and bestowing the blessing of longevity.',
            'Vô Lượng Thọ Phật — Hiện thân trường thọ tối thượng của Đức Phật A Di Đà.': 'Amitayus — The ultimate longevity emanation of Amitabha Buddha.',
            'Hoá thân phẫn nộ của Đức Đại Nhật Như Lai — Hàng phục ma chướng, bảo hộ hành giả trên con đường giác ngộ.': 'The wrathful emanation of Vairocana — Subduing demonic obstacles, protecting practitioners on the path to enlightenment.',
            'Hoàng Thần Tài Bồ Tát Zambhala — Ban phước thịnh vượng, viên mãn tài lộc.': 'Yellow Wealth Deity Zambhala — Bestowing prosperity and fulfilling wealth.',
            'Đại Thành Tựu Giả Nagabodhi — Đệ tử tâm truyền của Long Thọ Bồ Tát, truyền thừa Kim Cương Thừa.': 'Mahasiddha Nagabodhi — Heart disciple of Nagarjuna, Vajrayana lineage holder.',
            'Tài Bảo Thiên Vương — Một trong Tứ Đại Thiên Vương ': 'Vaishravana — One of the Four Heavenly Kings ',
            'Dự Án Xây Dựng Tu Viện': 'Monastery Construction Project',
            'Khôi phục tu viện huyền thoại Narthang tại Việt Nam — Nơi lưu giữ và truyền bá tinh hoa Phật giáo Kadam.': 'Restoring the legendary Narthang monastery in Vietnam — Preserving and propagating the essence of Kadam Buddhism.',
            'Lịch Sử Narthang Cổ': 'History of Ancient Narthang',
            'Hành trình ngàn năm của tu viện Narthang — Trung tâm ấn loát và học thuật vĩ đại nhất Tây Tạng.': 'The millennium journey of Narthang monastery — The greatest printing and academic center in Tibet.',
            'Gây Quỹ và Bảo Trợ': 'Fundraising and Sponsorship',
            'Chung tay góp gạch xây chùa, hộ trì Tam Bảo — Tích luỹ công đức vô lượng cho đời này và mai sau.': 'Join hands to build the temple, support the Three Jewels — Accumulate immeasurable merit for this life and the future.',
            'Ấn Kinh Narthang': 'Narthang Sutra Printing',
            'Phục hưng truyền thống in khắc mộc bản — Lưu truyền thánh giáo qua những trang kinh quý giá.': 'Reviving the woodblock printing tradition — Transmitting the holy teachings through precious sutra pages.',
            'Thư Viện Học Thuật': 'Academic Library',
            'Kho tàng tri thức Phật giáo đa ngữ — Nơi nghiên cứu và tu học của các hành giả hiện đại.': 'Multilingual Buddhist knowledge treasure — A place for modern practitioners to research and study.',
            'Truyền Thừa và Chư Đạo Sư': 'Lineage and Gurus',
            'Dòng chảy tâm linh bất đoạn — Từ Đức Phật Thích Ca Mâu Ni đến các bậc Thầy Narthang đương đại.': 'The uninterrupted spiritual stream — From Shakyamuni Buddha to the contemporary Narthang Masters.',
            'Trang chủ': 'Home'
        },
        'zh': {
            'OLD KADAMPA VN': 'OLD KADAMPA VN',
            'NARTHANG KADAMPA': '納唐噶當巴',
            'Hoá thân thành tựu sự nghiệp của Đại Thành Tựu Giả Tumton Lodro Drakpa — Người sáng lập tu viện Narthang Gompa.': '大成就者Tumton Lodro Drakpa的事業化身 — 納唐寺(Narthang Gompa)的創始人。',
            'Đại Luận Sư Atisha — Người phục hưng Phật Pháp tại Tây Tạng, khai sáng dòng truyền thừa Kadampa.': '阿底峽尊者 — 西藏佛教的復興者，噶當派的創始人。',
            'Đại Thành Tựu Giả Tumton Lodro Drakpa — Người sáng lập tu viện Narthang Gompa huyền thoại.': '大成就者Tumton Lodro Drakpa — 傳奇的納唐寺的創始人。',
            'Đức Phật Thích Ca Mâu Ni — Bậc Đạo Sư gốc của cõi Ta Bà, người khai sáng đạo Phật.': '釋迦牟尼佛 — 娑婆世界的根本導師，佛教的創始人。',
            'Đức Quán Thế Âm — Lòng từ bi bao trùm khắp tam giới.': '觀世音菩薩 — 慈悲遍佈三界。',
            'Đức Văn Thù Sư Lợi — Trí tuệ tỏa sáng xua tan màn vô minh.': '文殊菩薩 — 閃耀的智慧驅散無明的黑暗。',
            'Lục Độ Phật Mẫu Tara — Sinh ra từ giọt nước mắt bi mẫn của Đức Quán Thế Âm.': '綠度母 — 誕生於觀音菩薩慈悲的眼淚。',
            'Bạch Độ Phật Mẫu — Hiện thân của trường thọ, trí tuệ và sự bình an vô biên.': '白度母 — 長壽、智慧和無邊和平的化身。',
            'Dược Sư Lưu Ly Quang Vương Phật — Tiêu trừ bệnh tật, ban phước trường thọ.': '藥師琉璃光如來 — 消除疾病，賜予長壽。',
            'Vô Lượng Thọ Phật — Hiện thân trường thọ tối thượng của Đức Phật A Di Đà.': '無量壽佛 — 阿彌陀佛無上的長壽化身。',
            'Hoá thân phẫn nộ của Đức Đại Nhật Như Lai — Hàng phục ma chướng, bảo hộ hành giả trên con đường giác ngộ.': '大日如來的忿怒化身 — 降伏魔障，保護修行者在覺悟的道路上。',
            'Hoàng Thần Tài Bồ Tát Zambhala — Ban phước thịnh vượng, viên mãn tài lộc.': '黃財神 Zambhala — 賜福繁榮，圓滿財富。',
            'Đại Thành Tựu Giả Nagabodhi — Đệ tử tâm truyền của Long Thọ Bồ Tát, truyền thừa Kim Cương Thừa.': '大成就者龍智 — 龍樹菩薩的心子，金剛乘傳承者。',
            'Tài Bảo Thiên Vương — Một trong Tứ Đại Thiên Vương ': '多聞天王 — 四大天王之一 ',
            'Dự Án Xây Dựng Tu Viện': '寺廟建設計劃',
            'Khôi phục tu viện huyền thoại Narthang tại Việt Nam — Nơi lưu giữ và truyền bá tinh hoa Phật giáo Kadam.': '在越南恢復傳奇的納唐寺 — 保存和傳播噶當佛教的精華。',
            'Lịch Sử Narthang Cổ': '古納唐歷史',
            'Hành trình ngàn năm của tu viện Narthang — Trung tâm ấn loát và học thuật vĩ đại nhất Tây Tạng.': '納唐寺的千年旅程 — 西藏最偉大的印刷和學術中心。',
            'Gây Quỹ và Bảo Trợ': '籌款和贊助',
            'Chung tay góp gạch xây chùa, hộ trì Tam Bảo — Tích luỹ công đức vô lượng cho đời này và mai sau.': '攜手建寺，護持三寶 — 為今生和未來積累無量功德。',
            'Ấn Kinh Narthang': '納唐印經',
            'Phục hưng truyền thống in khắc mộc bản — Lưu truyền thánh giáo qua những trang kinh quý giá.': '復興木板印刷傳統 — 透過珍貴的經頁傳遞神聖教法。',
            'Thư Viện Học Thuật': '學術圖書館',
            'Kho tàng tri thức Phật giáo đa ngữ — Nơi nghiên cứu và tu học của các hành giả hiện đại.': '多語種佛教知識寶庫 — 現代修行者的研究和學習之地。',
            'Truyền Thừa và Chư Đạo Sư': '傳承與祖師',
            'Dòng chảy tâm linh bất đoạn — Từ Đức Phật Thích Ca Mâu Ni đến các bậc Thầy Narthang đương đại.': '不間斷的靈性之流 — 從釋迦牟尼佛到當代納唐大師。',
            'Trang chủ': '主頁'
        },
        'bo': {
            'NARTHANG KADAMPA': 'སྣར་ཐང་བཀའ་གདམས་པ།',
            'Trang chủ': 'ཡུལ་ངོས།'
        }
    }
    
    new_text = text
    # We also change the container id to avoid duplicate IDs
    new_text = new_text.replace('id="main-container"', f'id="main-container-{lang}"')
    
    for vi_str, translation in replacements.get(lang, {}).items():
        new_text = new_text.replace(vi_str, translation)
        
    return new_text

en_blocks = translate_block(original_blocks, 'en')
zh_blocks = translate_block(original_blocks, 'zh')
bo_blocks = translate_block(original_blocks, 'bo')

wrapped = f"""
        <div id="vi" class="lang-page active-page">
{original_blocks}
        </div>

        <div id="en" class="lang-page">
{en_blocks}
        </div>

        <div id="zh" class="lang-page">
{zh_blocks}
        </div>

        <div id="bo" class="lang-page">
{bo_blocks}
        </div>
"""

# Now we need to insert the .nav-sticky right before wrapped
# Wait, let's substitute the original containers in content
content = content.replace(original_blocks, wrapped)

# We also need to add CSS and the nav-sticky HTML and JS.

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
            color: var(--lotus-white);
            font-family: 'Montserrat', sans-serif;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
        }

        .flag-btn:hover,
        .flag-btn.active-btn {
            background: var(--wisdom-gold);
            color: #000;
            box-shadow: 0 0 15px var(--wisdom-gold);
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

content = content.replace('    </style>', css_to_add + '    </style>')

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

# Insert nav-sticky right before <div id="vi" class="lang-page active-page">
content = content.replace('        <div id="vi" class="lang-page active-page">', nav_html + '\n        <div id="vi" class="lang-page active-page">')

js_to_add = """
        function setLang(langId) {
            localStorage.setItem('selectedLanguage', langId);

            document.querySelectorAll('.lang-page').forEach(p => p.classList.remove('active-page'));
            const targetPage = document.getElementById(langId);
            if (targetPage) targetPage.classList.add('active-page');

            document.querySelectorAll('.flag-btn').forEach(btn => btn.classList.remove('active-btn'));
            const activeBtn = document.getElementById('btn-' + langId);
            if (activeBtn) activeBtn.classList.add('active-btn');
            
            // Handle subtitles in hover if necessary.
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        window.addEventListener('DOMContentLoaded', () => {
            const savedLang = localStorage.getItem('selectedLanguage') || 'vi';
            setLang(savedLang);
        });
"""

content = content.replace('    <script>', '    <script>' + js_to_add)

with open('/Users/yogiphil/Desktop/WEB DEVELOPMENT PROJECT/EXAMPLE1/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
