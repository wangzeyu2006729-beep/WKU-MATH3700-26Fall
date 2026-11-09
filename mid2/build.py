"""Build the self-contained Mid2 practice page."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text())

# IDs are assigned once and stored with the question to preserve browser progress.
questions = [
    dict(entry, chapter=chapter)
    for chapter, group in enumerate(data['groups'])
    for entry in group
]
assert len(questions) == len({q['label'] for q in questions})
assert len(questions) == len({q['id'] for q in questions})
for q in questions:
    assert q['text'] and q['zh']['text'] and q['explanation'] and q['note']
    assert q['kind'] in {'计算', '证明', '理论'}
    assert q['bank'] == 'written' and not q['options'] and not q['zh']['options']
    assert q['answer'] is None
    if q.get('origin') == 'bank':
        assert q['role'] == 'variant' and q['pair'] == 'Q' + q['label'][1:]

payload = {'chapters': data['chapters'], 'questions': questions, 'practiceOrder': [q['id'] for q in questions]}
html = (ROOT / 'template.html').read_text()
for marker, value in {
    '__MID2_DATA__': json.dumps(payload, ensure_ascii=False).replace('</', '<\\/'),
    '__TOTAL__': str(len(questions)),
    '__BANK_COUNT__': str(sum(q.get('origin') == 'bank' for q in questions)),
    '__TEXTBOOK_COUNT__': str(sum(q.get('origin') == 'textbook' for q in questions)),
}.items():
    assert marker in html
    html = html.replace(marker, value)
(ROOT / 'index.html').write_text(html)
print(f"Built Mid2 with {len(questions)} written questions")
for chapter, item in enumerate(data['chapters']):
    print(item['name'], sum(q['chapter'] == chapter for q in questions))
