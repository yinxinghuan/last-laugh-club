import path from 'node:path';
import { createRequire } from 'node:module';
const require=createRequire(import.meta.url);
const { chromium }=require('playwright');

async function accelerate(page){
 const video=page.locator('video');
 await video.waitFor({state:'visible',timeout:5000});
 await video.evaluate((element)=>{element.muted=true;element.playbackRate=16;void element.play()});
}

const browser=await chromium.launch({headless:true});
for(const viewport of [{width:390,height:844},{width:320,height:568}]){
 const page=await browser.newPage({viewport});
 await page.addInitScript(()=>localStorage.setItem('game_locale','zh'));
 await page.goto('http://127.0.0.1:4190/',{waitUntil:'networkidle'});
 await page.addStyleTag({content:'#alteru-guest-banner{display:none!important}'});
 const tag=`${viewport.width}x${viewport.height}`;
 await page.screenshot({path:path.resolve(`_qa/ui/platform-layout-cover-${tag}.png`)});
 await page.locator('.llc-cover>.llc-primary').dispatchEvent('pointerdown');
 await accelerate(page);
 await page.waitForSelector('.llc-question',{timeout:8000});
 await page.screenshot({path:path.resolve(`_qa/ui/platform-layout-question-${tag}.png`)});
 await page.getByText('让香槟自己作证',{exact:true}).dispatchEvent('pointerdown');
 await accelerate(page);
 await page.waitForSelector('.llc-verdict--success',{timeout:8000});
 await page.screenshot({path:path.resolve(`_qa/ui/platform-layout-success-${tag}.png`)});
}
await browser.close();
