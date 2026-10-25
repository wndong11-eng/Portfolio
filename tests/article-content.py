from pathlib import Path
import subprocess
import re
import html
from html.parser import HTMLParser

page = Path('index.html').read_text(encoding='utf-8')
original = subprocess.check_output(['git','show','main:index.html']).decode('utf-8').replace('\r\n','\n')
clean = re.sub(r'\n  <style id="article-styles">.*?</style>\n\n', '', page, flags=re.S)
clean = re.sub(r'\n  <!-- Advertising cooperation guide:.*?(?=  <!-- ==================== Contact Section)', '', clean, flags=re.S)
assert clean.strip() == original.strip(), 'Existing page changed outside article additions'
body = Path('articles/ad-agency-pricing.md').read_text(encoding='utf-8-sig').split('---',2)[2]
class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.bits=[]
    def handle_data(self,data): self.bits.append(data)
parser=Text(); parser.feed(page)
plain=re.sub(r'\s+','', ''.join(parser.bits))
for line in body.splitlines():
    line=line.strip()
    if not line or line=='---' or re.fullmatch(r'[|\- ]+',line): continue
    line=re.sub(r'^## |^- |^> ', '',line).replace('**','')
    for cell in line.strip('|').split('|'):
        assert re.sub(r'\s+','',cell) in plain, f'Missing original text: {cell}'
ids=re.findall(r'\bid="([^"]+)"',page)
assert len(ids)==len(set(ids)), 'Duplicate IDs'
print('PASS: original page preserved; all source paragraphs/table cells in static HTML; unique IDs')
