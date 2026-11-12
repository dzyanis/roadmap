const $ = id => document.getElementById(id);
let graph, svg, fullBox, selected = '', request = 0, manifest;
let anchors = new Map();
const state = () => new URLSearchParams(location.hash.slice(1));
function share() {
  const hash = new URLSearchParams({roadmap: $('roadmap').value, layout: $('layout').value});
  if (selected) hash.set('topic', selected);
  history.replaceState(null, '', `#${hash}`);
}
function box() { const b = svg.viewBox.baseVal; return [b.x,b.y,b.width,b.height]; }
function setBox(b) { svg.setAttribute('viewBox', b.join(' ')); }
function fit() { if (svg) setBox(fullBox); }
function zoom(factor, center) {
  if (!svg) return;
  const [x,y,w,h] = box();
  const next = Math.max(80, Math.min(fullBox[2] * 3, w * factor));
  const ratio = next / w;
  const [cx,cy] = center || [x+w/2,y+h/2];
  setBox([cx-(cx-x)*ratio, cy-(cy-y)*ratio, next, h*ratio]);
}
function point(event) {
  return new DOMPoint(event.clientX,event.clientY).matrixTransform(svg.getScreenCTM().inverse());
}
function focusTopic(anchor) {
  const b = anchor.getBBox();
  const matrix = svg.getScreenCTM().inverse().multiply(anchor.getScreenCTM());
  const first = new DOMPoint(b.x,b.y).matrixTransform(matrix);
  const last = new DOMPoint(b.x+b.width,b.y+b.height).matrixTransform(matrix);
  const ratio = $('viewport').clientWidth / $('viewport').clientHeight;
  const height = Math.max(340, Math.abs(last.y-first.y)+160, (Math.abs(last.x-first.x)+200)/ratio);
  setBox([(first.x+last.x)/2-height*ratio/2, (first.y+last.y)/2-height/2,height*ratio,height]);
}
function element(tag, text, parent) {
  const node = document.createElement(tag); node.textContent = text; parent.append(node); return node;
}
function safeLink(url, title, parent) {
  try {
    const parsed = new URL(url);
    if (!['https:','http:'].includes(parsed.protocol)) return;
    const link = element('a', title || url, parent);
    link.href = parsed.href; link.target = '_blank'; link.rel = 'noopener noreferrer';
  } catch { /* Invalid links remain in source data, but are not executable. */ }
}
function choose(id, focus = true, updateUrl = true) {
  const topic = graph.topics.find(t => t.id === id);
  if (!topic) { $('status').textContent = `Unknown topic: ${id}`; return; }
  selected = id;
  for (const [key, anchor] of anchors) anchor.classList.toggle('selected', key === id);
  for (const button of $('topics').querySelectorAll('button')) button.setAttribute('aria-current', String(button.dataset.topic === id));
  const details = $('details'); details.replaceChildren();
  element('h2', topic.label, details);
  element('p', topic.id, details).className = 'topic-id';
  element('h3', `Learning resources (${topic.resources.length})`, details);
  if (!topic.resources.length) element('p', 'No learning resources are attached to this topic yet.', details);
  const list = element('ul', '', details);
  for (const resource of topic.resources) {
    const li = element('li', '', list);
    safeLink(resource.url, resource.title || resource.url, li);
    element('span', ` · ${resource.type}${resource.language ? ' · '+resource.language : ''}`, li);
    if (resource.description) element('p', resource.description, li);
    if (resource.translation) safeLink(resource.translation.url, ` Translation (${resource.translation.language})`, li);
  }
  for (const [title, source, target] of [['Parents','target','source'],['Next topics','source','target']]) {
    const ids = [...new Set(graph.edges.filter(e => e[source] === id).map(e => e[target]))];
    if (!ids.length) continue;
    element('h3', title, details);
    for (const related of ids) {
      const button = element('button', graph.topics.find(t => t.id === related).label, details);
      button.className = 'connection'; button.onclick = () => choose(related);
    }
  }
  $('status').textContent = `Selected ${topic.label}. ${topic.resources.length} learning resources.`;
  if (focus && anchors.has(id)) focusTopic(anchors.get(id));
  if (updateUrl) share();
}
function search() {
  if (!graph) return;
  const query = $('search').value.trim().toLocaleLowerCase();
  const matches = graph.topics.filter(t => `${t.label} ${t.id}`.toLocaleLowerCase().includes(query));
  const matching = new Set(matches.map(t => t.id));
  for (const [id, anchor] of anchors) anchor.classList.toggle('match', !!query && matching.has(id));
  $('topics').replaceChildren();
  for (const topic of matches) {
    const li = element('li', '', $('topics'));
    const button = element('button', topic.label, li);
    button.dataset.topic = topic.id; button.setAttribute('aria-current', String(selected === topic.id));
    button.onclick = () => choose(topic.id);
  }
  $('status').textContent = `${matches.length} of ${graph.topics.length} topics. Select a result to focus it.`;
}
async function checkedFetch(path, type) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response[type]();
}
async function load(fromHash = false) {
  const token = ++request;
  const hash = state();
  const key = $('roadmap').value, layout = $('layout').value;
  const wanted = fromHash ? hash.get('topic') : selected;
  $('status').textContent = 'Loading map…';
  try {
    const [data, source] = await Promise.all([checkedFetch(`${key}.json`, 'json'), checkedFetch(`${key}-${layout}.svg`, 'text')]);
    if (token !== request) return;
    const parsed = new DOMParser().parseFromString(source,'image/svg+xml');
    if (parsed.querySelector('parsererror')) throw new Error('Invalid diagram SVG');
    graph = data; svg = document.importNode(parsed.documentElement,true);
    svg.setAttribute('aria-hidden','true');
    $('viewport').replaceChildren(svg); fullBox = box();
    anchors = new Map([...svg.querySelectorAll('a[data-topic]')].map(a => [a.dataset.topic,a]));
    if (anchors.size !== graph.topics.length) throw new Error('Diagram topic links do not match JSON');
    $('download').href = `${key}-${layout}.svg`;
    $('counts').textContent = `${graph.topics.length} topics · ${graph.edges.length} connections`;
    selected = ''; search();
    $('details').replaceChildren(); element('h2','Explore the map',$('details'));
    element('p','Select a topic to view its resources and connections.',$('details'));
    if (wanted) choose(wanted, true, false);
    if (!fromHash) share();
    $('viewport').dataset.ready = `${key}-${layout}`;
    performance.mark('roadmap-ready');
  } catch (error) {
    if (token !== request) return;
    svg = null; graph = null; anchors.clear(); $('viewport').replaceChildren();
    $('status').textContent = `Could not load map: ${error.message}`;
    delete $('viewport').dataset.ready;
  }
}
$('roadmap').onchange = () => { selected = ''; $('search').value = ''; load(); };
$('layout').onchange = () => load();
$('search').oninput = search;
$('search').onkeydown = event => { if (event.key === 'Enter') $('topics').querySelector('button')?.click(); };
$('fit').onclick = fit;
$('zoom-in').onclick = () => zoom(.75);
$('zoom-out').onclick = () => zoom(1/.75);
const viewport = $('viewport');
viewport.addEventListener('wheel', event => {
  if (!svg) return;
  event.preventDefault(); const p = point(event); zoom(Math.exp(Math.max(-1,Math.min(1,event.deltaY*.002))), [p.x,p.y]);
}, {passive:false});
let drag, moved = false;
viewport.addEventListener('pointerdown', event => {
  if (!svg || !event.isPrimary || event.button !== 0) return;
  viewport.focus({preventScroll:true});
  drag = {id:event.pointerId, x:event.clientX, y:event.clientY, box:box(), matrix:svg.getScreenCTM().inverse()}; moved = false;
});
viewport.addEventListener('pointermove', event => {
  if (!drag || drag.id !== event.pointerId) return;
  const distance = Math.hypot(event.clientX-drag.x,event.clientY-drag.y);
  if (!moved && distance < 4) return;
  moved = true; viewport.setPointerCapture(event.pointerId);
  const start = new DOMPoint(drag.x,drag.y).matrixTransform(drag.matrix);
  const end = new DOMPoint(event.clientX,event.clientY).matrixTransform(drag.matrix);
  setBox([drag.box[0]+start.x-end.x,drag.box[1]+start.y-end.y,...drag.box.slice(2)]);
});
for (const name of ['pointerup','pointercancel']) viewport.addEventListener(name, () => { drag = null; });
viewport.addEventListener('click', event => {
  const anchor = event.target.closest('a[data-topic]');
  if (anchor) { event.preventDefault(); if (!moved) choose(anchor.dataset.topic); }
  moved = false;
});
viewport.addEventListener('keydown', event => {
  if (!svg) return;
  const b = box(), step = b[2]*.1;
  if (event.key === '+' || event.key === '=') zoom(.75);
  else if (event.key === '-') zoom(1/.75);
  else if (event.key === 'Home') fit();
  else if (event.key === 'ArrowLeft') { b[0]-=step; setBox(b); }
  else if (event.key === 'ArrowRight') { b[0]+=step; setBox(b); }
  else if (event.key === 'ArrowUp') { b[1]-=step; setBox(b); }
  else if (event.key === 'ArrowDown') { b[1]+=step; setBox(b); }
  else return;
  event.preventDefault();
});
function applyHash() {
  const params = state();
  $('roadmap').value = manifest.some(m => m.id === params.get('roadmap')) ? params.get('roadmap') : 'dsa';
  $('layout').value = ['dagre','elk','graphviz'].includes(params.get('layout')) ? params.get('layout') : 'dagre';
  $('search').value = ''; load(true);
}
try {
  manifest = await checkedFetch('manifest.json','json');
  for (const item of manifest) { const option = element('option',item.label,$('roadmap')); option.value = item.id; }
  addEventListener('hashchange',applyHash); applyHash();
} catch (error) { $('status').textContent = `Could not load catalog: ${error.message}`; }
