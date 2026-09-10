// Local artifact QA only; no external browser navigation.
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/pietr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const file=path.resolve(process.argv[2]),out=path.dirname(file);
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const results=[];
 try{
  for(const width of [1440,390]){
   const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(pathToFileURL(file).href);
   const count=await page.locator('.panel').count();
   if(count!==22)throw Error(`Expected 22 panels; got ${count}`);
   const options=await page.locator('#pair option').count();
   for(let pair=0;pair<options;pair++){
    await page.selectOption('#pair',String(pair));
    if(await page.locator('.panel').count()!==22)throw Error('Pairing redraw failed');
    await page.locator('.panel svg').first().scrollIntoViewIfNeeded();
    const box=await page.locator('.panel svg').first().boundingBox();
    await page.mouse.move(0,0);
    await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
    const detail=await page.locator('.detail').first().innerText();
    if(!detail.includes('['))throw Error(`Tooltip failed: ${detail}`);
   }
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
   if(overflow)throw Error(`Page overflow at ${width}`);
   if(errors.length)throw Error(errors.join('\n'));
   await page.evaluate(()=>scrollTo(0,0));
   await page.screenshot({path:path.join(out,`qa_${width}.png`)});
   results.push({width,panels:count,pairings:options,errors,overflow});
   await page.close();
  }
 }finally{await browser.close();}
 fs.writeFileSync(path.join(out,'qa.json'),JSON.stringify(results,null,2)+'\n');
 console.log(JSON.stringify(results));
})().catch(e=>{console.error(e);process.exit(1)});
