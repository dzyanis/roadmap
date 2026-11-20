# Renderer decision evidence for #40

Recommendation for review: retain Graphviz SVG for the first implementation of
[#39](https://github.com/dzyanis/roadmap/issues/39) and retain Graphviz for static
exports. The same viewer provides the requested interaction with every renderer.
The alternatives have not demonstrated a navigation benefit that offsets their
larger layouts and additional build dependencies. **Mermaid Dagre is the preferred
alternative** if Mermaid authoring/Markdown reuse becomes a requirement.

This is a proposed decision, not an agreed production replacement. Both prototype
PRs remain independent experiments. Agree on the selection in #40 before merging
production changes. The proposed implementation scope is below.

## Comparable evidence

Both branches start at `adbbf53` (merged shared graph pipeline). They use the same
validated XML inputs, stable topic IDs, edges, resources, explicit 28-character
word wrapping, source-subject containers, LR orientation, and viewer code.
Shared descendants remain single nodes with multiple edges. The Graphviz baseline
is styled/grouped like the candidates, rather than copying the old production SVG.
All JSON and Graphviz source/SVG files match between branches. Renderer defaults
still differ in padding, font metrics and edge routing: these are configured
candidates rather than a pure algorithm benchmark.

| Input | Nodes | Edges | Resource associations |
| --- | ---: | ---: | ---: |
| dsa | 47 | 46 | 4 |
| os | 56 | 55 | 23 |
| go | 294 | 294 | 107 |
| devops | 188 | 188 | 56 |

Resource associations count each topic/resource attachment, including repeated
resources. JSON retains original unwrapped labels and all resource metadata.
MySQL has two incoming edges in Go and DevOps; no tree conversion duplicates it.

### Dimensions and output sizes

Each cell is **width × height; SVG KiB** (1024 bytes). Dimensions are rounded SVG
viewBox units, not screenshot pixels. Full sources, SVGs and exact measurements
are committed with each prototype.

| Input | Graphviz | Mermaid Dagre | Mermaid ELK | D2 Dagre | D2 ELK |
| --- | --- | --- | --- | --- | --- |
| dsa | 1119 × 1559; 36.9 | 1351 × 1898; 85.2 | 1313 × 2602; 81.9 | 1578 × 3611; 128.2 | 1638 × 2548; 129.2 |
| os | 996 × 2122; 49.6 | 1198 × 2837; 112.0 | 1230 × 3763; 110.4 | 1344 × 4991; 152.3 | 1674 × 3747; 153.5 |
| go | 1467 × 9186; 237.3 | 1683 × 13049; 499.1 | 1697 × 17123; 474.0 | 2220 × 24255; 715.7 | 2095 × 17100; 731.0 |
| devops | 1219 × 6475; 156.9 | 1403 × 8996; 332.4 | 1601 × 11784; 322.8 | 1814 × 16334; 466.7 | 2079 × 11651; 474.8 |

Graphviz has the smallest area for every input. Mermaid Dagre is shorter than
Mermaid ELK here; ELK is not automatically better. D2 ELK reduces the full-roadmap
height by about 30% relative to D2 Dagre, but remains taller than Graphviz.
Every full roadmap has unreadably small labels at fit-to-view: search-to-focus
and zoom are essential regardless of renderer.

### Measured costs

Measured on macOS 26.6.2 arm64, Python 3.9.6, Node 26.13.0, Graphviz 16.1.1,
Mermaid CLI 12.2.0 / Mermaid 12.3.0, D2 0.9.0, Chrome 157.0.8103.51. Final builds
and browser runs were serial on the same machine. Each cell is one warm-machine
run, with no statistical confidence or cold-start claim. Build timings include
process startup and renderer layout/export, excluding SVG metadata postprocessing.

| Input | Graphviz seconds | Mermaid Dagre / ELK seconds | D2 Dagre / ELK seconds |
| --- | ---: | ---: | ---: |
| dsa | 0.075 | 1.926 / 1.327 | 0.041 / 0.033 |
| os | 0.062 | 1.204 / 1.496 | 0.036 / 0.034 |
| go | 0.072 | 1.874 / 1.933 | 0.179 / 0.077 |
| devops | 0.073 | 1.509 / 1.598 | 0.097 / 0.057 |

- Mermaid: viewer HTML/CSS/JS 14,770 bytes; all demo assets 2,922,795 bytes. Navigation-to-viewer-ready 22–58 ms across 12 views.
- D2: viewer HTML/CSS/JS 14,760 bytes; all demo assets 3,891,560 bytes. Navigation-to-viewer-ready 23–319 ms across 12 views.

Browser measurements use fresh documents, disabled HTTP cache, localhost and a
1440 × 1000 viewport. `viewerReadyMs` ends after SVG insertion/initial selection;
it is not a paint/FPS measure. `browser-results.json` records resource timings and
transfer sizes. `elapsedIncludingNetworkIdleMs` includes interactions and the
network-idle wait and must not be treated as render time. No mobile network or
real-device performance benchmark was performed. D2 ELK's Go view was slower in
this run; one sample cannot establish typical latency.

Only the selected JSON and SVG are fetched. Neither candidate ships renderer
JS/WASM to visitors. The viewer is about 15 KB uncompressed; SVG dominates transfer
size. Demo totals include all layouts, sources and JSON, excluding previews and
metrics themselves.

## Evaluation matrix

| Criterion | Graphviz SVG baseline | Mermaid SVG | D2 SVG |
| --- | --- | --- | --- |
| Labels | Wrapped text; smallest map | Wrapped SVG text; `htmlLabels:false` avoids foreignObject | Wrapped text; embedded font; link badges add clutter |
| Grouping / crossings | Compact clusters; cross-subject links still span ranks | Colored subgraphs; Dagre clearer at whole-map scale here; explicit LR fixes single-subject orientation | Strong containers; ELK reduces tall gaps; cross-container links still span large distances |
| Pan / zoom / fit | Viewer code | Same viewer | Same viewer |
| Search / highlight / selection | Viewer + JSON + SVG links | Same; loose mode enables generated links | Same; public SVG links identify topics |
| Resources / multiple parents | All resources and parents from JSON | Same | Same |
| Collapse / expand | Needs DAG visibility policy and relayout | Same; live Mermaid rerender adds a runtime and may move the map | Same; static D2 needs precomputed views or another layout runtime |
| Desktop / mobile | Mouse/one-finger pan; toolbar zoom; responsive panel | Same | Same |
| Keyboard / accessibility | HTML topic index, relationships, resources, labeled controls, live status; arrow pan, +/−, Home | Same | Same |
| Share links / Pages | Relative assets, hash roadmap/layout/topic; `/roadmap/` tested | Same | Same |
| SVG / PNG | Native exports already in production | SVG and bounded browser PNG work | SVG works; native full-roadmap PNG fails; bounded browser PNG works |
| Build / CI | Existing Python, xmllint, dot | Adds locked npm dependencies and Chrome for SVG build | Adds checksum-pinned binary for SVG; Chrome for viewer tests/bounded PNG |
| Maintenance | Existing exporter plus viewer/adapter | Syntax escaping, browser/CLI updates and SVG adapter | Syntax escaping, binary updates, SVG adapter and PNG workaround |
| Licensing | Graphviz EPL-1.0 | Mermaid/CLI MIT; dependencies have their own licenses | D2 MPL-2.0; embedded fonts/dependencies retain their notices; no TALA |

Visual observations come from committed SVG/PNG and desktop/mobile screenshots.
No crossing count or user comprehension study was run. Both incoming MySQL edges
remain visible in the focused desktop preview. Pan keeps layout fixed; selection
zooms to a readable neighborhood. Full-map fit supports orientation, not reading.

The accessible outline is a flat topic index with parent/child navigation rather
than a duplicated ARIA tree: the model is a DAG. SVG is hidden from assistive
technology to avoid hundreds of duplicate links. Keyboard tests pass; a screen-
reader audit, Safari/Firefox, actual iOS/Android, pinch zoom, high-contrast and
reduced-motion testing remain follow-up work. Selection uses replaceState;
Back is not a topic-history feature. Branch collapse is assessed, not implemented.

## Earlier findings: updated evidence

- The older Go sample had 262 topics; current XML has 294 after OS expansion.
  Old sizes/times are not directly comparable. This run also wraps all renderer
  labels and links every topic to the viewer instead of only some resource URLs.
- Graphviz's compactness advantage is confirmed. Its SVG supports the same HTML
  navigation, so Markdown familiarity alone does not favor replacing it.
- Mermaid's `htmlLabels:false` remains useful for portable text. Explicit line
  breaks work in both layouts. Explicit LR inside subgraphs avoids a wide/shallow
  single-subject layout. Cross-group links may override subgraph direction, as
  documented upstream. Native Markdown-string autowrap was not used so all
  candidates receive the same line breaks.
- D2 0.9.0 native PNG fails for Go at **79,226 px (Dagre)** and **64,916 px (ELK)**,
  and DevOps at **52,360 / 42,994 px**, against a 32,768-pixel per-dimension limit.
  The native PNG includes a hyperlink appendix and raster scaling, so its frame
  exceeds the SVG viewBox. `--scale=0.2` gives identical dimensions/failures in this
  tested version, including for successful DSA exports. See the D2 `png-results.json`
  and `probe-png.py`. All four SVGs rasterize successfully through the bounded
  browser path, max 6000 px high, without a hyperlink appendix.
- GitHub's fenced Mermaid Markdown renderer has its own version/settings. These
  HTML results do not establish support for the same configuration or links on
  GitHub. D2 integration uses images or this HTML viewer, not a native D2 fence.

## Other candidates and proposed production scope

[Cytoscape.js](https://js.cytoscape.org/) merits a separate prototype if live branch
collapse/expansion or editing becomes required: it provides a graph runtime and
pan/zoom/selection APIs. It would still need the resource panel, URL state,
accessible HTML outline and an evaluated layout. No third prototype was built:
the two requested experiments demonstrate that static SVG covers the first site's
core navigation, while collapse remains optional. This is a scope decision,
not a claim that Cytoscape is slower or visually worse.

A custom [ELK.js](https://github.com/kieler/elkjs) viewer could relayout filtered
subgraphs, but ELK supplies layout rather than a complete accessible viewer.
Both experiments already test ELK-backed layout without establishing a compactness
advantage over Graphviz. Defer another runtime until live relayout is required.
TALA is excluded because it adds a separate commercial engine.

Proposed follow-up within #39, subject to agreement in #40:

1. Generate all seven roadmaps through the shared pipeline; retain Graphviz
   exports and add stable topic identity/links to site SVGs.
2. Extract one maintained viewer; retain search, resources, parent/child links,
   accessible HTML and direct links; test assets under `/roadmap/`.
3. Decide whether collapse is required. If yes, specify DAG semantics first:
   hide a shared descendant only if no visible incoming path reaches it, preserve
   selection where possible, and prototype relayout before choosing a runtime.
4. Audit keyboard/screen-reader behavior and real mobile browsers, add production
   Pages deployment with validation gates, and link it from the README.
5. Record the agreed renderer decision in #40. Preserve experiment evidence;
   avoid shipping two duplicate viewers as production.

Sources: [Mermaid flowcharts](https://mermaid.js.org/syntax/flowchart.html),
[Mermaid layouts](https://mermaid.ai/open-source/config/layouts.html),
[D2 layouts](https://d2lang.com/tour/layouts/),
[D2 exports](https://www.d2lang.com/tour/exports/),
[D2 license](https://github.com/d2lang/d2/blob/v0.9.0/LICENSE.txt),
[Mermaid license](https://github.com/mermaid-js/mermaid/blob/develop/LICENSE),
[Graphviz license](https://graphviz.org/license/).
Measurements and recommendations above come from this experiment, not upstream docs.
