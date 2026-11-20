# Renderer decision — issue #40

Status: adopted in [PR #50](https://github.com/dzyanis/roadmap/pull/50);
recorded here to resolve [#40](https://github.com/dzyanis/roadmap/issues/40).

Use **Cytoscape.js with Dagre for the interactive website** and retain
**Graphviz for committed DOT/SVG/PNG exports**. XML and the shared validated
JSON model remain the source of truth. Mermaid and D2 remain experiments.

## Evidence and decision

The two independent prototype PRs requested by #40 are complete:

- [Mermaid #48](https://github.com/dzyanis/roadmap/pull/48), merged, includes
  Dagre/ELK layouts, a runnable viewer, previews, browser checks and measurements.
- [D2 #49](https://github.com/dzyanis/roadmap/pull/49), closed without merging,
  contains the equivalent experiment and native PNG-limit probes. Its evidence
  remains available at
  [commit c2ff442](https://github.com/dzyanis/roadmap/tree/c2ff442147d597effa69b346a30ee8b85f3729c3/docs/prototypes/d2).
  Closing the experiment did not invalidate its findings or require bringing a
  second experimental viewer into the production tree.

Both experiments use the same DSA, OS, Go and DevOps inputs from the shared
pipeline at `adbbf53`, preserving shared descendants, labels and resources.
The [comparison matrix](prototypes/mermaid/COMPARISON.md) records configurations,
visual dimensions, build times, browser timings, output sizes, interactions,
accessibility/device limitations, licensing and maintenance costs.
The [earlier comparison](renderer-comparison/README.md) is a separate, older
input snapshot. Neither table describes the subsequently expanded database tree.

Graphviz produced the most compact static layouts in those experiments and
already supports native SVG/PNG exports. Mermaid Dagre was the strongest tested
static alternative. D2 ELK reduced height relative to D2 Dagre, but D2 0.9.0
native PNG still failed for full roadmaps; bounded SVG rasterization worked.
These results support retaining Graphviz for exports.

The prototype recommendation also proposed Graphviz SVG for the first website.
**PR #50 took a different production approach:** it renders JSON in Cytoscape
with Dagre, rather than fetching a pre-rendered SVG. The merged implementation
settles that choice. The decision here adopts that existing split; it does not
claim the prototypes selected Cytoscape or that Cytoscape won their benchmark.

Cytoscape supplies a graph runtime for pan/zoom, selection, incident-edge
highlighting and focus. The production application supplies the resource panel,
search, URL state, keyboard controls and accessible HTML topic outline. It
preserves each shared topic as one node with all incoming edges. These concrete
capabilities justify keeping the shipped implementation without another renderer
migration. Branch collapse, editing and live filtered relayout are not shipped
requirements and are not a claimed benefit of this implementation.

## Production tradeoffs

| Concern | Website: Cytoscape + Dagre | Static exports: Graphviz |
| --- | --- | --- |
| Input | Version 1 `graph.json`, validated during site build | Shared validated XML model exported to DOT |
| Layout | Browser, left-to-right Dagre; source-subject colors | Build-time `dot`; existing ungrouped layout |
| Interaction | Graph runtime plus application UI | Images and generated Markdown guide |
| Resources and links | All topic resources; roadmap/topic hash links | Guide lists resources; exported files remain browsable on GitHub |
| Dependencies | Vendored browser scripts, pinned in the checkout; no CDN | Existing Graphviz build dependency |
| Licensing | Cytoscape and plugin MIT; Dagre MIT, notices in `site/vendor/` | Graphviz EPL-1.0; see historical matrix |
| Maintenance cost | Maintain runtime, layout plugin, DOM UI and dependency updates | Maintain DOT exporter and build tooling |
| Main limit | Browser pays download/layout cost; HTML outline needed for accessible navigation | Full maps are tall and need zooming; no application interactions |

The website does not need Mermaid CLI, D2, Chrome or a server-side renderer for
visitors. It does run layout/rendering JavaScript in the browser. Vendoring avoids
a CDN dependency, not the browser runtime cost. Graphviz is still required to
build all repository outputs through `make site`'s `all` prerequisite.

No matched Cytoscape-versus-SVG render-time, bundle-size or usability benchmark
was performed in #48/#49. Do not reuse their SVG viewer timings as Cytoscape
measurements or infer superiority from them. The website's actual pinned
libraries and license notices are in [site/vendor](../site/vendor/).

## Implementation and remaining scope

The production follow-up anticipated by #40 is already implemented by #50:

- `tools/build_site.py` discovers committed JSON and writes relative site assets.
- `site/app.js` renders the graph and implements navigation and resources.
- `make site` builds all seven roadmaps and the website.
- `.github/workflows/pages.yml` validates, tests and builds PRs, deploying master
  to Pages under `/roadmap/` after a successful build.
- Repository tests check site generation, graph validation and relative paths;
  the prototype browser evidence applies to the experimental SVG viewers.

Optional future work includes matched production browser performance measurements,
real mobile and cross-browser testing, and a production screen-reader audit.
Those are verification gaps, not completed audits. Collapse/expansion requires a
separate DAG visibility policy, including shared descendants and selection
preservation, before implementation. A custom ELK.js viewer remains deferred;
layout alone does not supply the application's navigation or accessibility UI.
TALA remains excluded from the experiment because it adds a commercial engine.
Typed relationships and their viewer compatibility remain separately tracked in
[#46](https://github.com/dzyanis/roadmap/issues/46).

The renderer evaluation is complete. Future work should target a specific
production requirement or measured problem rather than keep #40 open for a
replacement that has already been decided and shipped.
