/* Roadmap Core viewer. Reads the graph.json exports produced by tools/build_site.py. */
(() => {
  'use strict';

  const DATA = 'data/';
  const DEFAULT_ROADMAP = 'roles/go-engineer';
  const PAN_STEP = 80;
  const FOCUS_ZOOM = 1;
  const UNASSIGNED_COLOR = '#6b7280';
  // Fixed colours keep each subject's colour the same on every roadmap.
  const SUBJECT_COLORS = {
    'computer-science': '#8c6d1f',
    'data-structures-algorithms': '#d55e00',
    databases: '#0072b2',
    devops: '#7b61ff',
    go: '#00add8',
    java: '#b07219',
    networking: '#009e73',
    'operating-systems': '#e69f00',
    php: '#4f5d95',
    python: '#3776ab',
    ruby: '#cc342d',
    'software-development': '#cc79a7',
  };
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const $ = (id) => document.getElementById(id);
  const ui = {
    select: $('roadmap-select'),
    canvas: $('canvas'),
    search: $('search'),
    searchCount: $('search-count'),
    status: $('status'),
    card: $('topic-card'),
    outline: $('outline'),
    outlineCount: $('outline-count'),
    legend: $('legend'),
    live: $('live'),
    zoomIn: $('zoom-in'),
    zoomOut: $('zoom-out'),
    fit: $('fit'),
    copyLink: $('copy-link'),
  };

  const state = {
    index: [],
    cache: new Map(),
    roadmapId: null,
    graph: null,
    topics: new Map(),
    cy: null,
    topicId: null,
    loadToken: 0,
  };

  /* ---------- small DOM helpers (textContent only, never innerHTML) ---------- */

  function el(tag, text, attributes = {}, children = []) {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = text;
    for (const [name, value] of Object.entries(attributes)) {
      if (value !== undefined && value !== null) node.setAttribute(name, value);
    }
    node.append(...children);
    return node;
  }

  function prettify(subject) {
    const words = subject.replace(/-/g, ' ');
    return words.charAt(0).toUpperCase() + words.slice(1);
  }

  function subjectColor(subject) {
    return SUBJECT_COLORS[subject] || UNASSIGNED_COLOR;
  }

  function topicColor(topic) {
    return topic.subjects.length ? subjectColor(topic.subjects[0]) : UNASSIGNED_COLOR;
  }

  function announce(message) {
    ui.live.textContent = '';
    ui.live.textContent = message;
  }

  function setStatus(message) {
    ui.status.textContent = message;
  }

  /* ---------- data ---------- */

  async function fetchJSON(path) {
    const response = await fetch(path, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
    return response.json();
  }

  async function loadRoadmap(id) {
    if (!state.cache.has(id)) {
      state.cache.set(id, fetchJSON(`${DATA}${id}.json`).then((graph) => {
        if (![1, 2].includes(graph.schema_version)) {
          throw new Error(`Unsupported graph version ${graph.schema_version}.`);
        }
        return graph;
      }));
    }
    return state.cache.get(id);
  }

  function populateSelect() {
    const groups = new Map();
    for (const entry of state.index) {
      const category = entry.id.split('/')[0];
      if (!groups.has(category)) groups.set(category, []);
      groups.get(category).push(entry);
    }
    const names = { roles: 'Engineer roles', technologies: 'Technologies', foundations: 'Foundations' };
    for (const [category, entries] of groups) {
      const group = el('optgroup', names[category] || prettify(category), { label: names[category] || prettify(category) });
      for (const entry of entries) {
        group.append(el('option', entry.label, { value: entry.id }));
      }
      ui.select.append(group);
    }
  }

  /* ---------- graph ---------- */

  function buildElements(graph) {
    const nodes = graph.topics.map((topic) => ({
      data: { id: topic.id, label: topic.label, color: topicColor(topic) },
    }));
    const edges = graph.edges.map((edge) => ({
      data: { id: edge.id, source: edge.source, target: edge.target, type: edge.type },
    }));
    return [...nodes, ...edges];
  }

  // Cytoscape's 'label' sizing is deprecated, so node boxes are sized from an estimate of the
  // wrapped label. Estimates are generous: the boxes are a little larger than the text, never smaller.
  const NODE_TEXT_WIDTH = 150;
  const CHARACTER_WIDTH = 7;
  const LINE_HEIGHT = 16;
  function wrappedLines(label) {
    const charactersPerLine = Math.floor(NODE_TEXT_WIDTH / CHARACTER_WIDTH);
    return Math.max(1, Math.ceil(label.length / charactersPerLine));
  }

  const STYLE = [
    {
      selector: 'node',
      style: {
        shape: 'round-rectangle',
        width: NODE_TEXT_WIDTH + 16,
        height: (node) => wrappedLines(node.data('label')) * LINE_HEIGHT + 16,
        padding: '8px',
        'background-color': '#ffffff',
        'border-color': 'data(color)',
        'border-width': 3,
        label: 'data(label)',
        'text-wrap': 'wrap',
        'text-max-width': '150px',
        'text-valign': 'center',
        'text-halign': 'center',
        'font-size': '12px',
        'font-family': 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif',
        color: '#111827',
      },
    },
    {
      selector: 'edge',
      style: {
        width: 1.5,
        'curve-style': 'bezier',
        'line-color': '#9ca3af',
        'target-arrow-shape': 'triangle',
        'target-arrow-color': '#9ca3af',
        'arrow-scale': 0.9,
      },
    },
    {
      selector: 'edge[type = "prerequisite"]',
      style: { 'line-style': 'dashed', label: 'Learn first', 'font-size': 10,
        'text-background-color': '#fff', 'text-background-opacity': 1 },
    },
    {
      selector: 'edge[type = "related-to"]',
      style: { 'line-style': 'dotted', 'target-arrow-shape': 'none', label: 'Related', 'font-size': 10,
        'text-background-color': '#fff', 'text-background-opacity': 1 },
    },
    { selector: '.hit', style: { 'background-color': '#fef08a' } },
    { selector: '.neighbor', style: { 'border-width': 5 } },
    {
      selector: '.selected',
      style: { 'background-color': '#111827', color: '#ffffff', 'border-width': 5 },
    },
    {
      selector: 'edge.active',
      style: { 'line-color': '#111827', 'target-arrow-color': '#111827', width: 2.5 },
    },
    { selector: '.dim', style: { opacity: 0.15 } },
  ];

  function layoutOptions() {
    return {
      name: 'dagre',
      rankDir: 'LR',
      nodeSep: 14,
      rankSep: 70,
      edgeSep: 8,
      padding: 30,
      animate: false,
      // The viewer chooses the initial view. A layout-driven fit would override it.
      fit: false,
    };
  }

  function destroyGraph() {
    if (state.cy) {
      state.cy.destroy();
      state.cy = null;
    }
  }

  function createGraph(graph) {
    destroyGraph();
    const cy = cytoscape({
      container: ui.canvas,
      elements: buildElements(graph),
      style: STYLE,
      minZoom: 0.05,
      maxZoom: 3,
      // Layout is fixed: dragging nodes would make the tree differ from the generated one.
      autoungrabify: true,
      boxSelectionEnabled: false,
    });
    // Place nodes using the outline. Other links can point across it in any direction.
    cy.nodes().union(cy.edges('[type = "contains"]')).layout(layoutOptions()).run();
    cy.on('tap', 'node', (event) => selectTopic(event.target.id(), { source: 'graph' }));
    cy.on('tap', (event) => {
      if (event.target === cy) clearSelection();
    });
    state.cy = cy;
    return cy;
  }

  /* ---------- selection and focus ---------- */

  function focusNode(node, { zoom = true } = {}) {
    const cy = state.cy;
    const box = node.renderedBoundingBox({ includeLabels: true });
    const inside = box.x1 >= 0 && box.y1 >= 0 && box.x2 <= cy.width() && box.y2 <= cy.height();
    const targetZoom = zoom ? Math.max(cy.zoom(), FOCUS_ZOOM) : cy.zoom();
    if (inside && targetZoom === cy.zoom()) return;
    cy.animate(
      { center: { eles: node }, zoom: targetZoom },
      { duration: reduceMotion ? 0 : 250 },
    );
  }

  function markGraph(topicId) {
    const cy = state.cy;
    cy.batch(() => {
      cy.elements().removeClass('selected neighbor active');
      if (!topicId) return;
      const node = cy.getElementById(topicId);
      node.addClass('selected');
      node.connectedEdges().addClass('active');
      node.connectedEdges().connectedNodes().not(node).addClass('neighbor');
    });
  }

  function markOutline(topicId) {
    for (const button of ui.outline.querySelectorAll('button')) {
      button.setAttribute('aria-current', button.dataset.id === topicId ? 'true' : 'false');
    }
  }

  function selectTopic(id, { source = 'outline', moveFocus = false } = {}) {
    const topic = state.topics.get(id);
    if (!topic || !state.cy) return;
    state.topicId = id;
    markGraph(id);
    markOutline(id);
    renderCard(topic);
    const node = state.cy.getElementById(id);
    if (source !== 'graph') focusNode(node);
    writeHash();
    const parents = neighbors(node, 'contains', 'target').length;
    const children = neighbors(node, 'contains', 'source').length;
    announce(`${topic.label}. ${parents} parent topics, ${children} subtopics, ${topic.resources.length} learning resources.`);
    if (moveFocus) document.getElementById('topic-title')?.focus({ preventScroll: true });
  }

  function clearSelection() {
    state.topicId = null;
    if (state.cy) markGraph(null);
    markOutline(null);
    ui.card.replaceChildren(
      el('h2', 'Choose a topic', { id: 'topic-title', tabindex: '-1' }),
      el('p', 'Select a topic on the map or in the list to see how it connects and its learning resources.'),
    );
    writeHash();
  }

  /* ---------- topic card ---------- */

  function relationList(topics) {
    const container = el('ul', null, { class: 'relation-list' });
    for (const topic of topics) {
      const button = el('button', topic.label, { type: 'button' });
      button.addEventListener('click', () => selectTopic(topic.id, { source: 'card', moveFocus: true }));
      container.append(el('li', null, {}, [button]));
    }
    return container;
  }

  function resourceItem(resource) {
    const meta = [resource.type && prettify(resource.type), resource.language].filter(Boolean).join(' · ');
    const children = [el('a', resource.title, { href: resource.url, target: '_blank', rel: 'noopener noreferrer' })];
    if (meta) children.push(el('div', meta, { class: 'resource-meta' }));
    if (resource.description) children.push(el('p', resource.description, { class: 'resource-description' }));
    if (resource.translation) {
      const language = resource.translation.language;
      children.push(el('div', null, {}, [
        el('a', `Translation (${language})`, {
          href: resource.translation.url, target: '_blank', rel: 'noopener noreferrer',
        }),
      ]));
    }
    return el('li', null, {}, children);
  }

  function neighbors(node, type, endpoint) {
    const ids = new Set();
    node.connectedEdges().forEach((edge) => {
      if (edge.data('type') !== type) return;
      const source = edge.data('source');
      const target = edge.data('target');
      if (endpoint !== 'target' && source === node.id()) ids.add(target);
      if (endpoint !== 'source' && target === node.id()) ids.add(source);
    });
    return [...ids].map((id) => state.topics.get(id));
  }

  function renderCard(topic) {
    const node = state.cy.getElementById(topic.id);
    const parents = neighbors(node, 'contains', 'target');
    const children = neighbors(node, 'contains', 'source');
    const sort = (list) => list.sort((a, b) => a.label.localeCompare(b.label));
    const subject = topic.subjects.length ? prettify(topic.subjects[0]) : 'Roadmap root';

    const title = el('h2', topic.label, { id: 'topic-title', tabindex: '-1' });
    const subjectLine = el('p', subject, { class: 'resource-meta' });
    const partOf = el('h3', 'Part of');
    const includes = el('h3', 'Includes');
    const resources = el('h3', `Learning resources (${topic.resources.length})`);

    const parentSection = [partOf, parents.length
      ? relationList(sort(parents))
      : el('p', 'Top-level topic.')];

    const childSection = [includes, children.length
      ? relationList(sort(children))
      : el('p', 'No subtopics.')];

    const extraSections = [
      ['Learn first', neighbors(node, 'prerequisite', 'target')],
      ['Learn next', neighbors(node, 'prerequisite', 'source')],
      ['Related topics', neighbors(node, 'related-to')],
    ].flatMap(([label, topics]) => topics.length ? [el('h3', label), relationList(sort(topics))] : []);

    const resourceSection = [resources];
    if (topic.resources.length) {
      resourceSection.push(el('ul', null, { class: 'resource-list' },
        topic.resources.map(resourceItem)));
    } else {
      resourceSection.push(el('p', 'No learning resources are attached to this topic yet.'));
    }

    ui.card.replaceChildren(title, subjectLine, ...parentSection, ...childSection, ...extraSections, ...resourceSection);
  }

  /* ---------- outline and search ---------- */

  function renderOutline(graph) {
    const items = [...graph.topics].sort((a, b) => a.label.localeCompare(b.label));
    ui.outline.replaceChildren(...items.map((topic) => {
      const button = el('button', topic.label, { type: 'button', 'aria-current': 'false' });
      button.dataset.id = topic.id;
      button.addEventListener('click', () => selectTopic(topic.id, { source: 'outline', moveFocus: true }));
      return el('li', null, {}, [button]);
    }));
    ui.outlineCount.textContent = `(${items.length})`;
  }

  function matches(topic, query) {
    return topic.label.toLowerCase().includes(query) || topic.id.toLowerCase().includes(query);
  }

  function applySearch() {
    const query = ui.search.value.trim().toLowerCase();
    const cy = state.cy;
    const hits = query ? new Set(state.graph.topics.filter((t) => matches(t, query)).map((t) => t.id)) : null;
    cy.batch(() => {
      cy.elements().removeClass('hit dim');
      if (hits) {
        cy.nodes().forEach((node) => {
          if (hits.has(node.id())) node.addClass('hit');
          else node.addClass('dim');
        });
        cy.edges().forEach((edge) => {
          if (!(hits.has(edge.source().id()) && hits.has(edge.target().id()))) edge.addClass('dim');
        });
      }
    });
    for (const item of ui.outline.children) {
      item.hidden = Boolean(hits) && !hits.has(item.firstElementChild.dataset.id);
    }
    if (!hits) {
      ui.searchCount.textContent = '';
      ui.outlineCount.textContent = `(${state.graph.topics.length})`;
      return hits;
    }
    ui.searchCount.textContent = hits.size ? `${hits.size} match${hits.size === 1 ? '' : 'es'}` : 'No matches';
    ui.outlineCount.textContent = `(${hits.size} of ${state.graph.topics.length})`;
    return hits;
  }

  function firstMatch() {
    const query = ui.search.value.trim().toLowerCase();
    if (!query) return null;
    return state.graph.topics
      .filter((t) => matches(t, query))
      .sort((a, b) => a.label.localeCompare(b.label))[0] || null;
  }

  /* ---------- legend ---------- */

  function renderLegend(graph) {
    const items = graph.subjects.map((subject) => el('span', prettify(subject), { class: 'legend-item' }, [
      el('span', null, { class: 'swatch', 'aria-hidden': 'true' }),
    ]));
    items.forEach((item, index) => {
      item.querySelector('.swatch').style.borderColor = subjectColor(graph.subjects[index]);
    });
    const hasRootOnly = graph.topics.some((t) => t.subjects.length === 0);
    if (hasRootOnly) {
      const unassigned = el('span', 'Roadmap topic', { class: 'legend-item' }, [
        el('span', null, { class: 'swatch', 'aria-hidden': 'true' }),
      ]);
      unassigned.querySelector('.swatch').style.borderColor = UNASSIGNED_COLOR;
      items.push(unassigned);
    }
    ui.legend.replaceChildren(el('span', 'Colour shows subject:', { class: 'legend-title' }), ...items);
  }

  /* ---------- roadmap switching and URL state ---------- */

  function readHash() {
    const params = new URLSearchParams(location.hash.slice(1));
    return { roadmap: params.get('roadmap'), topic: params.get('topic') };
  }

  function writeHash() {
    const params = new URLSearchParams();
    if (state.roadmapId) params.set('roadmap', state.roadmapId);
    if (state.topicId) params.set('topic', state.topicId);
    const hash = params.toString();
    history.replaceState(null, '', hash ? `#${hash}` : location.pathname + location.search);
  }

  let renderToken = 0;

  async function showRoadmap(id, topicId) {
    const token = ++renderToken;
    setStatus('Loading roadmap…');
    let graph;
    try {
      graph = await loadRoadmap(id);
    } catch (error) {
      setStatus(`Could not load this roadmap. ${error.message}`);
      return;
    }
    if (token !== renderToken) return;

    state.roadmapId = id;
    state.graph = graph;
    state.topics = new Map(graph.topics.map((t) => [t.id, t]));
    ui.select.value = id;
    document.title = `${graph.roadmap.label} · Roadmap Core`;

    createGraph(graph);
    renderOutline(graph);
    renderLegend(graph);
    state.topicId = null;
    clearSelection();
    applySearch();
    // Full maps are too tall to read at fit-to-view, so open at readable zoom on the root.
    state.cy.zoom(FOCUS_ZOOM);
    state.cy.center(state.cy.getElementById(graph.roadmap.root));
    setStatus(`${graph.roadmap.label}: ${graph.topics.length} topics, ${graph.edges.length} connections.`);

    if (topicId && state.topics.has(topicId)) {
      selectTopic(topicId, { source: 'url' });
    } else {
      writeHash();
    }
  }

  function resolveRoadmap(requested) {
    if (requested && state.index.some((entry) => entry.id === requested)) return requested;
    if (state.index.some((entry) => entry.id === DEFAULT_ROADMAP)) return DEFAULT_ROADMAP;
    return state.index[0].id;
  }

  async function applyHash() {
    const { roadmap, topic } = readHash();
    const id = resolveRoadmap(roadmap);
    if (roadmap && roadmap !== id) setStatus(`Unknown roadmap "${roadmap}". Showing ${id}.`);
    if (id === state.roadmapId && state.graph) {
      if (topic && state.topics.has(topic)) selectTopic(topic, { source: 'url' });
      else if (!topic) clearSelection();
      return;
    }
    await showRoadmap(id, topic);
  }

  /* ---------- controls ---------- */

  function zoomBy(factor) {
    const cy = state.cy;
    cy.zoom({
      level: cy.zoom() * factor,
      renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 },
    });
  }

  function bindControls() {
    ui.select.addEventListener('change', () => {
      state.topicId = null;
      showRoadmap(ui.select.value, null);
    });
    ui.zoomIn.addEventListener('click', () => zoomBy(1.25));
    ui.zoomOut.addEventListener('click', () => zoomBy(0.8));
    ui.fit.addEventListener('click', () => state.cy.animate({ fit: { eles: state.cy.elements(), padding: 30 } }, { duration: reduceMotion ? 0 : 250 }));
    ui.copyLink.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(location.href);
        setStatus('Link copied.');
      } catch {
        setStatus('Copy failed. The address bar already contains this link.');
      }
    });

    ui.search.addEventListener('input', () => {
      applySearch();
    });
    ui.search.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        const topic = firstMatch();
        if (topic) selectTopic(topic.id, { source: 'search', moveFocus: false });
      } else if (event.key === 'Escape') {
        ui.search.value = '';
        applySearch();
      }
    });

    ui.canvas.addEventListener('keydown', (event) => {
      const cy = state.cy;
      if (!cy) return;
      const pans = { ArrowLeft: [PAN_STEP, 0], ArrowRight: [-PAN_STEP, 0], ArrowUp: [0, PAN_STEP], ArrowDown: [0, -PAN_STEP] };
      if (pans[event.key]) {
        event.preventDefault();
        cy.panBy({ x: pans[event.key][0], y: pans[event.key][1] });
      } else if (event.key === '+' || event.key === '=') {
        event.preventDefault();
        zoomBy(1.25);
      } else if (event.key === '-' || event.key === '_') {
        event.preventDefault();
        zoomBy(0.8);
      } else if (event.key === 'Home') {
        event.preventDefault();
        cy.fit(undefined, 30);
      } else if (event.key === 'Escape') {
        clearSelection();
      }
    });

    document.addEventListener('keydown', (event) => {
      const typing = event.target instanceof HTMLElement && (event.target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(event.target.tagName));
      if (event.key === '/' && !typing) {
        event.preventDefault();
        ui.search.focus();
      }
    });

    window.addEventListener('hashchange', () => applyHash());
  }

  /* ---------- start ---------- */

  async function start() {
    ui.canvas.tabIndex = 0;
    ui.canvas.setAttribute('aria-describedby', 'legend');
    bindControls();
    try {
      state.index = await fetchJSON(`${DATA}index.json`);
    } catch (error) {
      setStatus(`The roadmap index could not be loaded (${error.message}). Serve this folder over HTTP to view it.`);
      return;
    }
    populateSelect();
    await applyHash();
    if (!location.hash) {
      writeHash();
    }
  }

  start();
})();
