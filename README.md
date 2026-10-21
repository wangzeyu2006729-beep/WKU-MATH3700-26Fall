# WKU3700Midquiz

**140 practice questions for Gupta's Fall 2027 MATH 3700 Mid Quiz at Wenzhou-Kean University.**

[Start practicing online](https://wangzeyu2006729-beep.github.io/WKU3700Midquiz/)

The bank combines **100 instructor-provided reference questions** with **40 independently written, slightly harder variants** based on the original questions and Weeks 1–5 lecture material. Questions are in English; explanations and study controls are in Chinese.

- **University:** Wenzhou-Kean University (WKU)
- **Course:** MATH 3700 — Big Data Computing
- **Instructor:** Gupta
- **Semester:** Fall 2027 (27Fall)
- **Coverage:** Big data foundations, linear algebra, matrix calculus and eigenvalues, probability, high-dimensional geometry, distance measures, and gradient descent/SGD.

This is an independent study aid. The variants are not instructor-issued questions or exam predictions.

![Dark practice interface](docs/preview.png)

## Practice

A compact dark interface keeps the question and choices at the center. Choose **全部** for all 140 questions, **原题** for the original 100, or **变式** for the additional 40. Combine a bank with a chapter filter, random practice, incorrect-answer review, or bookmarks.

- Original labels are **Q01–Q100**; variant labels are **V01–V40**.
- Search `Q12` or `V12` to find a specific question, or enter a keyword.
- Select an answer, then confirm to reveal the solution.
- Variants include source-question references, difficulty, worked Chinese explanations, and common pitfalls. Five challenge questions provide necessary formulas in the stem.
- Answering a missed question correctly removes it from incorrect-answer review when the list is refreshed.
- Restarting a group hides solutions while retaining previous records.
- Keyboard: `1`–`4` or `A`–`D` select; `Enter` confirms or continues; arrow keys navigate; `S` bookmarks.

## Private progress and upgrades

Answers, drafts, bookmarks, and position stay in **the current browser's localStorage**, under `math3700-practice-v1`. There is no backend, account, tracking, or answer upload.

The original 100 questions keep their internal IDs. Existing online progress continues after this update; a saved 100-question queue expands to include the new variants while keeping the current question, answers, attempts, and drafts. Variant internal IDs are 101–140, displayed as V01–V40.

Different devices, browsers, and browser profiles have independent records. Tabs within one browser profile share the record. Clearing browser data removes progress; private-window records may disappear after closing. There is no cross-device synchronization. The former separate offline variant page has its own browser storage and is not automatically imported across origins.

If storage is unavailable, the page shows a warning and remains usable for that session.

## Offline use

Download `index.html` and open it in a browser. It contains the entire app and all questions, with no runtime dependencies or network requirement. Offline and online copies have separate browser storage.

## Sources and build

- `source.txt`: original text supplied from Gupta's **MATH 3700: Big Data Computing — 100-Question Multiple-Choice Quiz**.
- `build.py`: parses the original text, repairs extracted notation, adds Chinese explanations, and merges the variants.
- `variants.json`: independently written variants with original-question references and difficulty metadata.
- `questions.json`: generated merged bank.
- `template.html`: interface and browser behavior.
- `index.html`: generated standalone page deployed by GitHub Pages.

The original 100 question texts, choice order, answer-key choices, explanations, and ambiguity notes are preserved. Notes for Q3, Q58, Q64–65, Q88, and Q90 explain source wording or extraction ambiguities. Q64–65 use the standard error supplied in the question; Q90 uses `acfdeg`.

Rebuild using Python 3:

```bash
python3 build.py
```

## Verification

Serve the repository locally:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Use a dedicated disposable browser session for checks. `verify-browser.js` clears that session's practice progress. `verify-merge.js` and `verify-isolation.js` use independent browser contexts.

```bash
npx --yes --package @playwright/cli playwright-cli -s=wku3700 open http://127.0.0.1:8000/index.html
npx --yes --package @playwright/cli playwright-cli -s=wku3700 run-code --filename verify-browser.js
npx --yes --package @playwright/cli playwright-cli -s=wku3700 run-code --filename verify-merge.js
npx --yes --package @playwright/cli playwright-cli -s=wku3700 run-code --filename verify-isolation.js
```

These checks cover grading and navigation through all 140 questions, original/variant filters, upgrade compatibility, browser isolation, persistence, storage-denied operation, and layouts from 320 to 1440 pixels. See `docs/verification.json` for the verified run.

## License and attribution

Application code is available under the [MIT License](LICENSE). The original course materials retain their respective authors' rights; the code license does not relicense them. See [CONTENT_NOTICE.md](CONTENT_NOTICE.md).
