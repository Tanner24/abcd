import os
import re

dr = '/Users/yogiphil/Desktop/WEB DEVELOPMENT PROJECT/EXAMPLE1/pages/'
files = [f for f in os.listdir(dr) if f.endswith('.html')]

for f in files:
    with open(os.path.join(dr, f), 'r', encoding='utf-8') as file:
        content = file.read()
        
    # extract body content without scripts
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if not body_match:
        print(f"No body in {f}")
        continue
        
    body_content = body_match.group(1)
    
    # We want to identify the tags inside body.
    # Let's just find the index of the last mantra-pillar or speed-control or bg-overlay
    idx = -1
    for marker in ['</div>\n    <div class="mantra-pillar pillar-right">', 
                   '</div>\n    <div class="lineage-pillar pillar-right">',
                   '</div>\n    <div class="wrapper">', # maybe wrapper?
                   '<div id="mantra-r" class="pillar-content"></div>\n    </div>',
                   '<div id="mantra-r" class="pillar-content"></div>\n        </div>\n    </div>',
                   '<div class="speed-control">',
                   '</label>\n        <input type="range" id="speed-slider" min="0.1" max="8" step="0.1" value="1.5">\n    </div>']:
        pos = body_content.find(marker)
        if pos != -1:
            # find end of the marker block
            block_end = pos + len(marker)
            if block_end > idx:
                idx = block_end

    if idx == -1:
        print(f"{f}: Could not find a known marker to split content.")
    else:
        # print the next 50 chars after the marker to see the content wrapper
        next_chars = body_content[idx:idx+150].strip()
        print(f"{f}: Starts with: {next_chars.splitlines()[0] if next_chars else 'EMPTY'}")

