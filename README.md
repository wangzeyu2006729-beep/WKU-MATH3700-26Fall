# WKU3700Midquiz

**MATH 3700 · 习题间** — a self-contained, offline quiz app for Big Data Computing revision.

100 道英文课程题目，配中文界面与解析。零运行时依赖，不需要账号或后端。

![桌面刷题界面](docs/preview.png)

## 快速开始

下载仓库（Code → Download ZIP）并解压，或运行：

```bash
git clone https://github.com/wangzeyu2006729-beep/WKU3700Midquiz.git
cd WKU3700Midquiz
```

直接用 Chrome、Safari 或 Edge 打开 **index.html** 即可刷题。不用安装软件、运行服务器或联网；复制这一个 HTML 文件即可携带全部题库。

## 刷题方式

- **顺序练习**：按原题号做题，自动恢复题目位置和未提交的选项。
- **随机练习**：在当前章节及搜索范围内打乱题目，开启新一轮作答。
- **错题本**：收集每题最近一次答错的记录。进入时隐藏旧答案；答对后从错题库移出。本轮列表保留到重新进入，以便查看解析。
- **我的收藏**：点击题目右上角星标，集中复习收藏题。
- **章节 / 搜索**：按 7 个章节筛选；输入 Q35、35 或英文关键词搜索。筛选与当前模式同时生效。
- **重新练习本组 / 再答一次**：隐藏答案以便重新作答，保留累计记录；新的提交替换该题最近一次结果。
- **小结**：最后一题可查看当前组的已提交数量、答对数量、正确率与未答题数。

选择后点击「确认答案」才会揭示正确选项与中文解析。方向键切题；1–4 或 A–D 选择；Enter 提交或进入下一题；S 收藏。手机可以使用章节下拉菜单与可点击题号。

## 进度与数据

记录保存在当前浏览器的 localStorage，键名为 `math3700-practice-v1`，不上传。概览按每题最近一次提交计算：已练习 / 100、答对数、待巩固数、正确率。

同一浏览器、同一文件路径打开时可恢复记录；移动文件、更换浏览器、使用隐私模式或清除浏览数据可能导致记录不可用。HTTP 预览与直接打开文件的记录分别保存。浏览器禁止 localStorage 时会明确显示提示。

清空学习记录需要在页面弹窗中确认。移动端可从「?」说明弹窗清空记录。

## 题库来源与整理

- 用户提供的原始文本完整保留在 `source.txt`。
- 100 道题的题号、选项顺序、正确答案沿用原始题库。
- 整理复制导致丢失的上下标、矩阵换行、分数与幂，不加载外部公式库。
- 中文解析为补充说明。Q3、Q58、Q64–65、Q88、Q90 的原题排版或措辞问题在对应解析中提示；Q64–65 按题目给定标准误作答，Q90 的字符串依答案表整理为 `acfdeg`。
- 课程名称与原题保留英文，界面与解析使用中文。

## 文件与验证

`index.html` 是最终独立文件。`template.html` 为界面源码，`build.py` 从文本提取题目并整理公式，`questions.json` 为可检查的题库。修改源码后运行：

```bash
python3 build.py
```

浏览器行为检查脚本是 `verify-browser.js`，供 Playwright CLI 的 `run-code` 执行。2026-10-17 已通过 39 项 Chrome 浏览器检查，包括全部 100 题的评分、进度恢复、错题与收藏、筛选和 320–1440px 布局；也已验证直接以 `file://` 打开 HTML。验证摘要保存在 [docs/verification.json](docs/verification.json)。本地运行日志和测试截图在 `output/playwright/`，不纳入版本控制。

如需重新运行浏览器检查，先在仓库根目录启动本地服务：

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

在另一个终端运行（需要 Node.js / npm）：

```bash
npx --yes --package @playwright/cli playwright-cli -s=wku3700 open http://127.0.0.1:8000/index.html
npx --yes --package @playwright/cli playwright-cli -s=wku3700 run-code "$(cat verify-browser.js)"
```

这些检查会清空该测试浏览器的练习记录，请使用单独的测试会话。

## 许可证与来源

应用代码使用 [MIT License](LICENSE)。课程题目与原答案表的权利归原作者所有，MIT 许可不重新授权这些课程材料，具体见 [CONTENT_NOTICE.md](CONTENT_NOTICE.md)。本项目是独立复习工具。
