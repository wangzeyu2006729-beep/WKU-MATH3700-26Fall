async page => {
  const browser=page.context().browser(), checks=[];
  const contexts=[];
  const assert=(ok,name)=>{if(!ok)throw new Error(name);checks.push(name);};
  const read=p=>p.evaluate(()=>JSON.parse(localStorage.getItem('math3700-practice-v1')));
  try {
    const context=await browser.newContext();contexts.push(context);
    await context.addInitScript(()=>{
      if(!localStorage.getItem('math3700-practice-v1')) localStorage.setItem('math3700-practice-v1',JSON.stringify({answers:{1:{choice:'D',correct:true,attempts:3}},favorites:[88],mode:'all',chapter:'all',order:Array.from({length:100},(_,i)=>i+1),index:11,drafts:{12:'C'},retry:[],query:''}));
    });
    const old=await context.newPage();await old.goto(page.url());
    let s=await read(old);
    assert(s.answers[1].correct&&s.answers[1].attempts===3&&s.favorites[0]===88&&s.drafts[12]==='C','Original answers, attempts, favorites and drafts survive the upgrade');
    assert(s.order.length===140&&new Set(s.order).size===140&&s.order[s.index]===12,'Legacy 100-question queue expands to 140 and preserves current question');
    assert(await old.locator('.option.selected').getAttribute('data-choice')==='C','Legacy draft is restored in the question UI');
    await old.reload();s=await read(old);
    assert(s.order.length===140&&s.answers[1].attempts===3,'Migration is idempotent across refresh');
    assert((await old.locator('#done-stat').textContent()).includes('/ 140'),'Progress denominator includes both banks');
    await old.locator('[data-bank="original"]').click();
    assert((await read(old)).order.length===100,'Original filter contains exactly 100 questions');
    await old.locator('[data-bank="variants"]').click();
    assert((await read(old)).order.join()===Array.from({length:40},(_,i)=>i+101).join(),'Variant filter contains exactly 40 unique stable IDs');
    assert((await old.locator('.question-id').textContent()).includes('V01'),'Variant label starts at V01');
    await old.locator('#chapter-select').selectOption('3');
    assert((await read(old)).order.join()===Array.from({length:10},(_,i)=>116+i).join(),'Variant bank and probability chapter combine correctly');
    await old.locator('#chapter-select').selectOption('all');
    await old.locator('#search').fill('V24');
    assert((await read(old)).order.join()==='124','V24 search resolves to its variant ID');
    await old.locator('[data-choice="A"]').click();await old.locator('#submit').click();
    assert((await old.locator('.source-note').textContent()).includes('Q69')&&(await old.locator('.question-id').textContent()).includes('挑战'),'Variant provenance and difficulty are visible');
    await old.reload();
    assert((await read(old)).bank==='variants'&&(await read(old)).answers[124].correct,'Variant filter and answer survive refresh');
    await old.locator('[data-bank="all"]').click();await old.locator('#search').fill('Q24');
    assert((await read(old)).order.join()==='24','Q24 and V24 resolve to different questions');
    await old.locator('#search').fill('Q124');
    assert((await read(old)).order.length===0,'Invalid original labels cannot alias a variant');
    await old.locator('#search').fill('V41');
    assert((await read(old)).order.length===0,'Invalid variant labels have no results');
    await old.locator('#search').fill('V01');await old.locator('[data-choice="A"]').click();await old.locator('#submit').click();await old.locator('#bookmark').click();
    await old.locator('#search').fill('');await old.locator('[data-mode="wrong"]').click();
    assert((await read(old)).order.join()==='101','Wrong-answer review includes variant errors without mixing original IDs');
    await old.locator('[data-mode="saved"]').click();
    assert((await read(old)).order.join()==='88,101','Bookmarks from both banks coexist');
    await old.locator('[data-mode="all"]').click();await old.locator('[data-bank="variants"]').click();await old.locator('[data-mode="random"]').click();
    assert((await read(old)).order.length===40&&(await read(old)).order.every(id=>id>=101),'Random mode respects the variant filter');
    await old.setViewportSize({width:390,height:844});await old.locator('[data-mode="all"]').click();await old.locator('#search').fill('V23');
    assert(!(await old.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),'Long A/B variant fits mobile without horizontal overflow');
    await old.locator('[data-choice="C"]').click();await old.locator('#submit').click();
    await old.evaluate(()=>{document.activeElement.blur();window.scrollTo(0,0);});
    await old.screenshot({path:'output/playwright/mobile-variant.png',fullPage:true,animations:'disabled'});
    await old.locator('#search').fill('V11');await old.locator('[data-choice="C"]').click();await old.locator('#submit').click();
    await old.setViewportSize({width:1440,height:1050});await old.evaluate(()=>{document.activeElement.blur();window.scrollTo(0,0);});
    await old.screenshot({path:'output/playwright/desktop-variant.png',fullPage:true,animations:'disabled'});
    const bg=await old.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor);
    assert(bg==='rgb(17, 19, 21)','Dark background is applied');
    return {passed:checks.length,checks};
  } finally {await Promise.all(contexts.map(c=>c.close()));}
}
