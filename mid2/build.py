"""Build the offline Mid2 page from curated exercises and variants."""

import json
from itertools import count
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text())

questions = []
question_ids = count(1)
for chapter, group in enumerate(data['groups']):
    for entry in group:
        question_id = next(question_ids)
        # Reserve the removed Q slots so existing answers and drafts still use the same IDs.
        if isinstance(entry, str):
            assert entry in {f'Q{i:02d}' for i in range(45, 101)}
            continue
        questions.append(dict(entry, id=question_id, chapter=chapter))

labels = {q['label']: q for q in questions}
assert len(questions) == len(labels)
bank_variants = [q for q in questions if q.get('origin') == 'bank']
assert {q['label'] for q in bank_variants} == {f'M{i:02d}' for i in range(45, 101)}
assert all(q['role'] == 'variant' and q['pair'] == 'Q' + q['label'][1:] for q in bank_variants)
for i, q in enumerate(questions):
    assert q['text'] and q['zh']['text'] and q['explanation'] and q['note']
    assert q['kind'] in {'计算', '证明', '理论'}
    if q['bank'] == 'mc':
        assert len(q['options']) == len(q['zh']['options']) == 4
        assert q['answer'] in {'A', 'B', 'C', 'D'}
    else:
        assert q['bank'] == 'written' and not q['options'] and q['answer'] is None
    if q.get('role') == 'original':
        variant = questions[i+1]
        assert variant['label'] == q['pair'] and variant['pair'] == q['label']
        assert q['chapter'] == variant['chapter']

payload = {'chapters': data['chapters'], 'questions': questions, 'practiceOrder': [q['id'] for q in questions]}
mc = sum(q['bank'] == 'mc' for q in questions)
html = (ROOT / 'template.html').read_text()
for marker, value in {
    '__MID2_DATA__': json.dumps(payload, ensure_ascii=False).replace('</', '<\\/'),
    '__TOTAL__': str(len(questions)),
    '__MC_COUNT__': str(mc),
    '__WRITTEN_COUNT__': str(len(questions) - mc),
}.items():
    assert marker in html
    html = html.replace(marker, value)
(ROOT / 'index.html').write_text(html)
print(f"Built Mid2 with {len(questions)} questions ({mc} multiple choice, {len(questions)-mc} written)")
for chapter, item in enumerate(data['chapters']):
    print(item['name'], sum(q['chapter'] == chapter for q in questions))
