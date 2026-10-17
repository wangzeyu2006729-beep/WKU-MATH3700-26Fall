async (page) => {
  const browser = page.context().browser();
  const contexts = [await browser.newContext(), await browser.newContext()];
  const checks = [];
  const requests = [];
  const assert = (value, message) => { if (!value) throw new Error(message); checks.push(message); };
  const read = target => target.evaluate(() => JSON.parse(localStorage.getItem('math3700-practice-v1')));
  try {
    const [a,b] = await Promise.all(contexts.map(context => context.newPage()));
    for (const target of [a,b]) target.on('request', request => requests.push({method:request.method(),url:request.url()}));
    await Promise.all([a.goto(page.url()),b.goto(page.url())]);
    assert(Object.keys((await read(a)).answers).length===0 && Object.keys((await read(b)).answers).length===0, 'Two independent browsers start with empty records');
    await a.locator('[data-choice="D"]').click();
    await a.locator('#submit').click();
    await a.locator('#bookmark').click();
    await b.locator('#map [data-index="1"]').click();
    await b.locator('[data-choice="A"]').click();
    await b.locator('#submit').click();
    const firstA = await read(a), firstB = await read(b);
    assert(firstA.answers[1].correct && !firstA.answers[2], 'Browser A retains only its own answer');
    assert(!firstB.answers[2].correct && !firstB.answers[1], 'Browser B retains only its own answer');
    assert(firstA.favorites.includes(1) && firstB.favorites.length===0, 'Favorites are isolated');
    assert(await a.locator('#wrong-count').textContent()==='0' && await b.locator('#wrong-count').textContent()==='1', 'Wrong books are isolated');
    await Promise.all([a.reload(),b.reload()]);
    assert((await read(a)).answers[1].correct && !(await read(b)).answers[2].correct, 'Both independent records survive refresh');
    await a.locator('#reset').click();
    await a.locator('#confirm-reset').click();
    await b.reload();
    assert(Object.keys((await read(a)).answers).length===0 && Object.keys((await read(b)).answers).length===1, 'Clearing A leaves B progress intact');
    assert(requests.every(request=>request.method==='GET' && new URL(request.url).origin===new URL(page.url()).origin), 'No answer-upload requests or third-party tracking requests');
    return {url:page.url(),passed:checks.length,checks,networkRequests:requests.length};
  } finally {
    await Promise.all(contexts.map(context=>context.close()));
  }
}
