const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/pietr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const file=path.resolve(process.argv[2]),out=path.dirname(file),results=[];
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 try{for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(file).href);
  const panels=await page.locator('.panel svg').count();if(panels!==22)throw Error('Missing panels');
  await page.locator('.panel svg').first().focus();await page.keyboard.press('ArrowRight');
  if(!(await page.locator('.detail').first().innerText()).includes('D13'))throw Error('Keyboard detail failed');
  await page.locator('button[data-series="top770"]').click();
  if(await page.locator('button[data-series="top770"]').getAttribute('aria-pressed')!=='false')throw Error('Toggle failed');
  await page.locator('button[data-series="top770"]').click();
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
  if(errors.length||overflow)throw Error(JSON.stringify({errors,overflow}));
  await page.screenshot({path:path.join(out,`qa_${width}.png`)});
  results.push({width,panels,errors,overflow,keyboard:true,toggle:true});await page.close();
 }}finally{await browser.close()}
 fs.writeFileSync(path.join(out,'qa.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results));
})().catch(e=>{console.error(e);process.exit(1)});
