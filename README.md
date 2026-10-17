# WKU3700Midquiz

**Reference questions for Gupta's Fall 2027 MATH 3700 Mid Quiz at Wenzhou-Kean University.**

This interactive study tool is based on the reference-question PDF provided by Gupta for **MATH 3700: Big Data Computing, Fall 2027 (27Fall)**. It presents the PDF's 100 multiple-choice questions and answer key in a browser, with Chinese study explanations and individually saved practice progress.

**[Start practicing online](https://wangzeyu2006729-beep.github.io/WKU3700Midquiz/)** — no account or installation required.

- **University:** Wenzhou-Kean University (WKU)
- **Course:** MATH 3700 — Big Data Computing
- **Instructor:** Gupta
- **Semester:** Fall 2027 (27Fall)
- **Material:** Mid Quiz reference questions from the instructor-provided PDF
- **Coverage:** Weeks 1–5, 100 questions across seven topics

This is an independent study aid for working through the reference questions.

![Quiz interface preview](docs/preview.png)

## Features

- Sequential and randomized practice.
- Review of incorrect answers and bookmarked questions.
- Seven topic filters, question-number search, and keyword search.
- Answer confirmation before revealing the correct choice and explanation.
- Automatic restoration of progress, current position, and unsubmitted selections.
- Responsive desktop and mobile layouts, keyboard shortcuts, and practice summaries.
- A self-contained HTML file with no runtime dependencies or backend.

The original questions remain in English. The app interface and supplementary explanations are in Chinese.

## Independent progress

Everyone uses the same public question bank, while answers, incorrect-answer records, and bookmarks are saved **only in their own browser's localStorage**. The app does not upload practice records or share them with other learners.

Different devices, browsers, and browser profiles have independent records. Tabs in the same browser profile use the same local record. If several people share a computer, use separate browser profiles. There are no accounts or cross-device synchronization; clearing browser data removes progress, and private-window records may disappear when the session closes.

The online site and a downloaded HTML file use separate storage. If browser storage is unavailable, the app displays a warning and remains usable for the current session. Resetting progress requires confirmation.

## Use offline

Download and extract this repository using **Code → Download ZIP**, or clone it:

```bash
git clone https://github.com/wangzeyu2006729-beep/WKU3700Midquiz.git
cd WKU3700Midquiz
```

Open `index.html` in a browser. You can copy this single file to another device and practice offline without running a server.

## Controls

Select an option, then confirm your answer to reveal the explanation.

| Shortcut | Action |
| --- | --- |
| `1`–`4` or `A`–`D` | Select an answer |
| `Enter` | Confirm the answer or continue |
| Left / right arrow | Move between questions |
| `S` | Toggle the bookmark |

Incorrect answers enter the review list automatically. Answering correctly removes a question from that list when it is refreshed. Restarting a question or group hides its solutions while retaining existing records until the next submission. Statistics use the most recent submission for each question.

## Source material and editorial notes

The question bank comes from Gupta's provided PDF, titled **MATH 3700: Big Data Computing — 100-Question Multiple-Choice Quiz**. The supplied text is preserved in `source.txt`; the structured question bank is in `questions.json`.

Question numbers, answer-choice order, and answer-key choices are preserved. Formatting repairs restore superscripts, fractions, matrix layouts, and line breaks lost during text extraction. Chinese explanations are supplementary study notes.

Notes attached to Q3, Q58, Q64–65, Q88, and Q90 explain source wording or formatting ambiguities. Q64–65 follow the standard error stated in the questions. Q90 uses `acfdeg`, consistent with the supplied answer key.

## Build and verification

Edit `template.html` for the interface or `build.py` for question parsing and notation repairs, then rebuild:

```bash
python3 build.py
```

The generated `index.html` embeds the entire question bank. The app has passed 39 browser checks covering all 100 questions, grading, progress restoration, review modes, and layouts from 320 to 1440 pixels. The verification summary is in [docs/verification.json](docs/verification.json). The deployed site also passed eight independent-browser isolation checks.

To run the browser checks, start a local server:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

In another terminal, with Node.js and npm available:

```bash
npx --yes --package @playwright/cli playwright-cli -s=wku3700 open http://127.0.0.1:8000/index.html
npx --yes --package @playwright/cli playwright-cli -s=wku3700 run-code "$(cat verify-browser.js)"
npx --yes --package @playwright/cli playwright-cli -s=wku3700 run-code "$(cat verify-isolation.js)"
```

Use a dedicated test session: `verify-browser.js` resets its test browser's records. `verify-isolation.js` creates two separate browser sessions and checks that answers, bookmarks, incorrect-answer review, refresh, and resets remain independent. Local test outputs are excluded from version control.

## License and attribution

Application code is available under the [MIT License](LICENSE). The course questions and original answer key remain the materials of their respective authors; the application's MIT License does not relicense them. See [CONTENT_NOTICE.md](CONTENT_NOTICE.md) for attribution and scope. This project is not an official university website or an assertion of university endorsement.
