import { mkdir } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require=createRequire(import.meta.url);const {chromium}=require('playwright');
const browser=await chromium.launch({headless:true});const output=new URL('./ui/',import.meta.url);await mkdir(output,{recursive:true});
async function accelerate(page){const video=page.locator('video');await video.waitFor({state:'visible',timeout:5000});await video.evaluate(el=>{el.muted=true;el.playbackRate=16;void el.play()})}
async function shot(page,name){await page.screenshot({path:fileURLToPath(new URL(name,output)),fullPage:true})}
const routes=[/让香槟自己作证/,/让雨来评价这条裙子/,/让旧音乐盒选择她的舞伴/];
for(const viewport of [{width:390,height:844},{width:320,height:568}]){
 const page=await browser.newPage({viewport});await page.addInitScript(()=>localStorage.setItem('game_locale','zh'));await page.goto('http://127.0.0.1:4190/',{waitUntil:'networkidle'});await page.addStyleTag({content:'#alteru-guest-banner{display:none!important}'});const size=`${viewport.width}x${viewport.height}`;
 await shot(page,`platform-layout-cover-${size}.png`);await page.locator('.llc-cover>.llc-primary').click();
 for(let index=0;index<routes.length;index++){await accelerate(page);await page.waitForSelector('.llc-question');await shot(page,`platform-layout-story${index+1}-question-${size}.png`);await page.getByRole('button',{name:routes[index]}).click();await accelerate(page);await page.waitForSelector('.llc-verdict--success');await shot(page,`platform-layout-story${index+1}-success-${size}.png`);if(index<routes.length-1)await page.locator('.llc-verdict .llc-primary').click()}
 await page.close();
}
await browser.close();
