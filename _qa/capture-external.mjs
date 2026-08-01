import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require=createRequire(import.meta.url);const {chromium}=require('playwright');
const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:390,height:844}});
await page.goto('http://127.0.0.1:4190/',{waitUntil:'networkidle'});await page.waitForTimeout(1200);
await page.screenshot({path:fileURLToPath(new URL('./ui/external-guest-cover-390x844.png',import.meta.url)),fullPage:true});
await browser.close();
