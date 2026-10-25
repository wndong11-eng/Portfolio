const { chromium } = require('C:/Users/Master/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');
(async () => {
  const browser = await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const url = pathToFileURL(path.resolve(__dirname, '../index.html')).href;
  const results = [];
  try {
    for (const width of [1440, 390, 320]) {
      const page = await browser.newPage({viewport:{width,height:960},reducedMotion:'reduce'});
      await page.goto(url);
      const details = page.locator('#ad-pricing-article');
      await details.waitFor({timeout:5000});
      assert.equal(await details.getAttribute('open'), null);
      const summary = details.locator('summary');
      await summary.focus(); await page.keyboard.press('Enter');
      assert.equal(await details.evaluate(e=>e.open),true);
      assert.equal(await details.locator('.article-prose h3').count(),3);
      assert(await details.locator('.article-prose').innerText().then(t=>t.includes('單一廣告組合的月最低預算')));
      await details.locator('a[href="#article-scope"]').click();
      assert.equal(await details.evaluate(e=>e.open),true);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
      await details.locator('[data-close-article]').click();
      assert.equal(await details.evaluate(e=>e.open),false);
      assert.equal(await summary.evaluate(e=>e===document.activeElement),true);
      await summary.click();
      assert.equal(await details.locator('a.article-contact').getAttribute('href'),'#contact');
      if(width!==320){
        await page.locator('#insights').scrollIntoViewIfNeeded();
        await page.screenshot({path:path.resolve(__dirname,`../../article-expanded-${width}.png`)});
        await details.locator('[data-close-article]').click();
        await page.locator('#insights').scrollIntoViewIfNeeded();
        await page.screenshot({path:path.resolve(__dirname,`../../article-collapsed-${width}.png`)});
      }
      results.push({width,keyboard:true,anchors:true,collapseFocus:true,noHorizontalOverflow:true});
      await page.close();
    }
    const context = await browser.newContext({javaScriptEnabled:false});
    const page = await context.newPage(); await page.goto(url);
    await page.locator('#ad-pricing-article summary').click();
    assert(await page.locator('.article-prose').isVisible());
    results.push({javascriptDisabled:'native expansion and text readable'});
    fs.writeFileSync(path.resolve(__dirname,'../../article-checks.json'),JSON.stringify(results,null,2));
    console.log(JSON.stringify(results,null,2));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
