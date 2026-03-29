import os
import re
import json
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator

# Configuration
SOURCE_DIR = "/Users/yogiphil/Desktop/WEB DEVELOPMENT PROJECT/EXAMPLE1"
PAGES_DIR = os.path.join(SOURCE_DIR, "pages")
LANGS = ['en', 'zh', 'bo']
LANG_MAP = {
    'en': 'en',
    'zh': 'zh-CN',
    'bo': 'bo'
}

# Persistent cache across files
CACHE_FILE = "/Users/yogiphil/Desktop/WEB DEVELOPMENT PROJECT/EXAMPLE1/translation_cache.json"
cache = {}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)

# Flag HTML to inject if missing
NAV_STICKY_HTML = """
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

def get_translator(target_lang):
    return GoogleTranslator(source='vi', target=LANG_MAP[target_lang])

def translate_batch(texts, target_lang):
    if not texts:
        return {}
    
    unique_texts = list(set(t.strip() for t in texts if t.strip() and len(t.strip()) > 1))
    to_translate = [t for t in unique_texts if f"{target_lang}:{t}" not in cache]
    
    if to_translate:
        print(f"  Translating {len(to_translate)} new strings to {target_lang}...")
        try:
            # GoogleTranslator.translate_batch might be limited, let's use a safe chunk size
            batch_size = 30
            translator = get_translator(target_lang)
            for i in range(0, len(to_translate), batch_size):
                chunk = to_translate[i:i + batch_size]
                results = translator.translate_batch(chunk)
                for orig, trans in zip(chunk, results):
                    cache[f"{target_lang}:{orig}"] = trans
            
            # Save cache periodically
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  Batch translation error: {e}")

    return {t: cache.get(f"{target_lang}:{t}", t) for t in unique_texts}

def collect_strings(node, strings):
    if isinstance(node, NavigableString):
        if node.parent.name not in ['script', 'style']:
            text = str(node).strip()
            if text and len(text) > 1 and not any(c in text for c in "ཨོཾ་"):
                strings.add(str(node))
    elif hasattr(node, 'children'):
        for child in node.children:
            collect_strings(child, strings)

def apply_translations(node, translations):
    if isinstance(node, NavigableString):
        if node.parent.name not in ['script', 'style']:
            text = str(node).strip()
            if text in translations:
                node.replace_with(translations[text])
    elif hasattr(node, 'children'):
        for child in list(node.children):
            apply_translations(child, translations)

def fix_csp(soup):
    csp = soup.find('meta', attrs={'http-equiv': 'Content-Security-Policy'})
    if csp:
        content = csp['content']
        required = [
            "https://flagcdn.com",
            "https://upload.wikimedia.org",
            "https://scontent.fhan2-4.fna.fbcdn.net",
            "https://rinchenshop.com",
            "https://rinchenshop.at",
            "https://thethangka.com"
        ]
        dirty = False
        for r in required:
            if r not in content:
                content = content.replace("img-src 'self'", f"img-src 'self' {r}")
                content = content.replace("img-src", f"img-src {r}")
                dirty = True
        if dirty:
            csp['content'] = content

def process_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    fix_csp(soup)
    
    # Ensure nav-sticky
    if not soup.find('div', class_='nav-sticky'):
        body = soup.find('body')
        if body:
            container = soup.find('div', class_='container')
            if container:
                container.insert_before(BeautifulSoup(NAV_STICKY_HTML, 'html.parser'))
            else:
                body.insert(0, BeautifulSoup(NAV_STICKY_HTML, 'html.parser'))

    vi_div = soup.find('div', id='vi')
    if not vi_div:
        # Check if they have a main container to wrap
        container = soup.find('div', class_='container')
        if container:
            new_vi = soup.new_tag('div', id='vi', attrs={'class': 'lang-page active-page'})
            container.wrap(new_vi)
            vi_div = soup.find('div', id='vi')

    if vi_div:
        # Collect all strings once
        strings = set()
        collect_strings(vi_div, strings)
        
        last_node = vi_div
        for lang in LANGS:
            # Translate batch
            lang_translations = translate_batch(list(strings), lang)
            
            # Find or create lang div
            lang_div = soup.find('div', id=lang)
            if lang_div:
                lang_div.decompose()
            
            # Clone VI div
            new_lang_div = BeautifulSoup(str(vi_div), 'html.parser').find('div')
            new_lang_div['id'] = lang
            new_lang_div.attrs['class'] = 'lang-page' # Remove active-page
            
            # Apply
            apply_translations(new_lang_div, lang_translations)
            
            last_node.insert_after(new_lang_div)
            last_node = new_lang_div

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

def main():
    # Process index.html at root
    index_path = os.path.join(SOURCE_DIR, "index.html")
    if os.path.exists(index_path):
        process_file(index_path)
    
    # Process all pages in /pages/
    if os.path.exists(PAGES_DIR):
        for filename in sorted(os.listdir(PAGES_DIR)):
            if filename.endswith(".html"):
                process_file(os.path.join(PAGES_DIR, filename))

if __name__ == "__main__":
    main()
