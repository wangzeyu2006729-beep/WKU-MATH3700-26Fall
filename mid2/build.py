"""Build the offline Mid2 page from curated questions and the original quiz bank."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text())
reference = json.loads((ROOT.parent / 'questions.json').read_text())['questions']
bank = {q['label']: q for q in reference if q['bank'] == 'original'}
theory = {
    45, 47, 48, 50, 53, 56, 57, 58, 60, 63, 66, 69, 72, 73,
    75, 78, 82, 83, 84, 89, 92, 97, 99, 100,
}

questions = []
for chapter, group in enumerate(data['groups']):
    for entry in group:
        if isinstance(entry, str):
            base = bank[entry]
            item = dict(base, bank='mc', role='original', origin='bank',
                        pair=f"M{base['id']:02d}",
                        kind='理论' if base['id'] in theory else '计算',
                        note='原 100 题 · '+entry+('。'+base['note'] if base['note'] else ''))
        else:
            item = dict(entry)
        item.update(id=len(questions) + 1, chapter=chapter)
        questions.append(item)

labels = {q['label']: q for q in questions}
assert len(questions) == len(labels)
assert {q['label'] for q in questions if q.get('origin') == 'bank' and q['role'] == 'original'} == {
    f'Q{i:02d}' for i in range(45, 101)
}
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
