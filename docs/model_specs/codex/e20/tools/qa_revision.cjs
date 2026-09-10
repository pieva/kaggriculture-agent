const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/pietr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const file=path.resolve(process.argv[2]),out=path.dirname(file);
 const summary=process.argv.includes('--summary');
 const browser=await chromium.launch({headless:true,channel:'chrome'}),results=[];
 try{
  for(const width of [1440,390]){
   const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];
   page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(file).href);
   const panels=await page.locator('article svg').count();
   if(!summary&&panels!==22)throw Error(`Expected 22 KPI panels: ${panels}`);
   if(summary&&(await page.locator('main h1').count()!==1||await page.locator('table').count()<3))throw Error('Incomplete summary');
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
   if(errors.length||overflow)throw Error(JSON.stringify({errors,overflow,width}));
   const tooltips=await page.locator('svg circle title').count();
   const models=await page.locator('#legend span').count();
   if(!summary&&tooltips!==22*30*models)throw Error('Missing daily data tooltips');
   await page.screenshot({path:path.join(out,`qa_${width}.png`)});
   results.push({width,panels,tooltips,errors,overflow});await page.close();
  }
 }finally{await browser.close()}
 fs.writeFileSync(path.join(out,'qa.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results));
})().catch(e=>{console.error(e);process.exit(1)});
