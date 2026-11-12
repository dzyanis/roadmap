// Run after build.py. Hosts the demo under the GitHub Pages project subpath.
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {dirname, join, resolve, extname} from 'node:path';
import {fileURLToPath} from 'node:url';
const {default: puppeteer} = await import(process.env.PUPPETEER_MODULE || 'puppeteer');
const here = dirname(fileURLToPath(import.meta.url));
const demo = join(here, 'demo'), previews = join(here, 'previews');
await mkdir(previews, {recursive:true});
const basePath = `/roadmap/docs/prototypes/${here.split('/').at(-1)}/demo/`;
const mime = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'};
const server = createServer(async (req,res) => {
  try {
    const pathname = new URL(req.url, 'http://localhost').pathname;
    if (!pathname.startsWith(basePath)) {res.writeHead(404).end();return;}
    const path = resolve(demo, decodeURIComponent(pathname.slice(basePath.length)) || 'index.html');
    if (!path.startsWith(demo + '/')) {res.writeHead(403).end();return;}
    res.setHeader('Content-Type',mime[extname(path)] || 'application/octet-stream');
    res.end(await readFile(path));
  } catch {res.writeHead(404).end();}
});
await new Promise(r => server.listen(0,'127.0.0.1',r));
const url = `http://127.0.0.1:${server.address().port}${basePath}`;
let browser;
try {
  browser = await puppeteer.launch({headless:true, executablePath:process.env.PUPPETEER_EXECUTABLE_PATH,
    args:process.env.CI ? ['--no-sandbox'] : []});
  const page = await browser.newPage();
  await page.setViewport({width:1440,height:1000});
  const errors = []; page.on('pageerror',error => errors.push(error.message));
  await page.setCacheEnabled(false);
  const results = [];
  async function ready(key,engine) {
    await page.waitForFunction(value => document.getElementById('viewport').dataset.ready === value, {}, `${key}-${engine}`);
  }
  async function visit(target, options) {
    await page.goto('about:blank');
    await page.goto(target, options);
    await page.evaluate(() => document.fonts.ready);
  }
  const getBox = () => page.$eval('#viewport svg',el => el.getAttribute('viewBox').split(/\s+/).map(Number).join(' '));
  for (const key of ['dsa','os','go','devops']) {
    for (const engine of ['graphviz','dagre','elk']) {
      const start = performance.now();
      await visit(`${url}#roadmap=${key}&layout=${engine}`, {waitUntil:'networkidle0'});
      await ready(key,engine);
      const navigation = await page.evaluate(() => ({
        viewerReadyMs: performance.getEntriesByName('roadmap-ready').at(-1).startTime,
        domContentLoadedMs: performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd,
        assets: performance.getEntriesByType('resource').filter(r => !r.name.endsWith('favicon.ico')).map(r => ({name:r.name.split('/').at(-1),bytes:r.transferSize,durationMs:r.duration}))
      }));
      const snapshot = await page.evaluate(() => {
        const nodes = [...document.querySelectorAll('#viewport a[data-topic]')];
        return {nodes:nodes.length, outline:document.querySelectorAll('#topics button').length,
          invisible:nodes.filter(n => {const b=n.getBBox();return !b.width || !b.height;}).length,
          foreignObjects:document.querySelectorAll('#viewport foreignObject').length,
          overflow:document.documentElement.scrollWidth > innerWidth};
      });
      assert.equal(snapshot.nodes,snapshot.outline); assert.equal(snapshot.invisible,0);
      assert.equal(snapshot.foreignObjects,0); assert.equal(snapshot.overflow,false);
      const initial = await getBox(); await page.click('#zoom-in'); assert.notEqual(await getBox(),initial);
      await page.click('#fit'); assert.equal(await getBox(),initial);
      await page.focus('#viewport'); await page.keyboard.press('ArrowRight'); assert.notEqual(await getBox(),initial);
      await page.keyboard.press('Home'); assert.equal(await getBox(),initial);
      const rect = await page.$eval('#viewport', el => {const r=el.getBoundingClientRect();return {x:r.x+100,y:r.y+100};});
      await page.mouse.move(rect.x,rect.y); await page.mouse.down();
      await page.mouse.move(rect.x+40,rect.y+20,{steps:5}); await page.mouse.up();
      assert.notEqual(await getBox(),initial); await page.click('#fit');
      // Exercise real hit testing on a rendered node after using the outline to locate it.
      await page.click('#topics button');
      const topic = await page.$eval('#topics button', el => el.dataset.topic);
      await page.click(`#viewport a[data-topic="${topic}"]`);
      assert.equal(new URLSearchParams((await page.evaluate(() => location.hash)).slice(1)).get('topic'),topic);
      results.push({input:key,layout:engine,elapsedIncludingNetworkIdleMs:Math.round(performance.now()-start),...navigation,...snapshot});
    }
  }
  // Discover the stable ID from the model instead of assuming a naming convention.
  const go = JSON.parse(await readFile(join(demo,'go.json'),'utf8'));
  const mysql = go.topics.find(t => t.label === 'MySQL');
  assert.ok(mysql);
  await visit(`${url}#roadmap=go&layout=elk&topic=${encodeURIComponent(mysql.id)}`,{waitUntil:'networkidle0'});
  await ready('go','elk');
  assert.equal(await page.$eval('#details h2',el=>el.textContent),'MySQL');
  assert.equal(go.edges.filter(e=>e.target===mysql.id).length,2);
  assert.ok(await page.$$eval('#details .connection',els=>els.length) >= 2);
  await page.evaluate(() => scrollTo(0,0));
  assert.ok(await page.$eval('header',el=>el.getBoundingClientRect().bottom) > 0);
  assert.ok(await page.$eval('#viewport',el=>el.clientHeight) < 1000);
  await page.screenshot({path:join(previews,'desktop.png')});
  await page.click('#fit');
  await page.screenshot({path:join(previews,'overview.png')});
  await page.type('#search','operating systems');
  assert.ok(await page.$$eval('#topics button',els=>els.length) >= 1);
  await page.keyboard.press('Enter');
  assert.equal(await page.$eval('#details h2',el=>el.textContent),'Operating Systems');
  assert.ok(await page.$$eval('#details a',els=>els.length) > 0);
  assert.equal(await page.$$eval('#details a',els=>els.every(a=>a.target==='_blank' && a.rel.includes('noopener'))),true);
  const permalink = page.url(); await page.reload({waitUntil:'networkidle0'}); await ready('go','elk');
  assert.equal(page.url(),permalink); assert.equal(await page.$eval('#details h2',el=>el.textContent),'Operating Systems');
  await page.setViewport({width:390,height:844,isMobile:true,hasTouch:true,deviceScaleFactor:1});
  await visit(`${url}#roadmap=os&layout=elk&topic=os_processes`,{waitUntil:'networkidle0'});
  await ready('os','elk');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth),false);
  let initial = await getBox(); await page.tap('#zoom-in'); assert.notEqual(await getBox(),initial);
  const touch = await page.target().createCDPSession();
  const bounds = await page.$eval('#viewport',el=>{const r=el.getBoundingClientRect();return {x:r.x+100,y:r.y+100};});
  initial = await getBox();
  await touch.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[bounds]});
  await touch.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:bounds.x+50,y:bounds.y+50}]});
  await touch.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  assert.notEqual(await getBox(),initial);
  await page.screenshot({path:join(previews,'mobile.png'),fullPage:true});
  // Bounded raster export: same SVG, no renderer-specific PNG frame-size limit.
  await page.setViewport({width:1440,height:1000,isMobile:false,hasTouch:false});
  for (const key of ['dsa','os','go','devops']) {
    await visit(`${url}${key}-elk.svg`,{waitUntil:'load'});
    const dimensions = await page.$eval('svg',el=>{const b=el.viewBox.baseVal;return {w:b.width,h:b.height};});
    const scale = Math.min(1,6000/dimensions.h,3000/dimensions.w);
    const width=Math.ceil(dimensions.w*scale), height=Math.ceil(dimensions.h*scale);
    await page.setViewport({width,height,deviceScaleFactor:1});
    await page.screenshot({path:join(previews,`${key}-elk.png`)});
  }
  assert.deepEqual(errors,[]);
  await writeFile(join(here,'browser-results.json'),JSON.stringify({browser:await browser.version(),node:process.version,
    method:'Fresh document, HTTP cache disabled, localhost, 1440×1000; asset timings are Resource Timing. elapsed includes interactions and the networkidle0 wait, not a render benchmark.',
    tested:['12 graph/layout combinations','topic link coverage and nonempty bounds','no foreignObject','zoom / fit / keyboard pan','mouse and touch pan','diagram topic click','search + Enter','resources + safe new-tab links','two incoming MySQL edges','topic permalink reload','390px mobile overflow','bounded PNG exports'],results},null,2)+'\n');
  console.log(`Passed: ${results.length} views, desktop/mobile interactions, resources, deep links and PNG exports.`);
} finally { if (browser) await browser.close(); await new Promise(r=>server.close(r)); }
