# Roadmap renderer comparison

Keep Graphviz for full roadmaps. It produced the most compact layout for both
inputs, exported PNG directly, and already fits the build. Mermaid is a useful
option for smaller diagrams embedded in Markdown. D2's styling and containers
are worth revisiting if there is demand for a separate presentation format.

The experiment exports the same nodes and edges from the DSA subject and the
full Go Engineer roadmap. It groups the Go nodes by source subject and attaches the first
available learning resource to each node. The production build uses its
existing ungrouped Graphviz layout. Both inputs retain their original labels.
The Go graph also includes MySQL as a shared descendant of two database topics.

| Input | Nodes / edges | Graphviz `dot` | Mermaid Dagre | D2 Dagre |
| --- | ---: | --- | --- | --- |
| DSA subject | 47 / 46 | [SVG](samples/dsa-graphviz.svg), 1326 × 1502 | [SVG](samples/dsa-mermaid.svg), 976 × 2668 | [SVG](samples/dsa-d2.svg), 1827 × 3670 |
| Go stack | 262 / 262 | [SVG](samples/go-graphviz.svg), 1882 × 7793 | [SVG](samples/go-mermaid.svg), 1278 × 15847 | [SVG](samples/go-d2.svg), 2595 × 21296 |

Dimensions are the SVG viewBox rounded to whole units. Open the SVG directly
to zoom or try the resource links. Each subject sample has one distinct URL,
and each Go sample has 44 distinct URLs across 46 linked nodes. The Markdown
learning guides still list all resources.

- **Graphviz** uses narrow ranks and compact clusters. Long labels widen the
  oval nodes, but remain on one line. The full roadmap is tall even with this
  layout and needs zooming. The Go sample is about 167 KiB. Both PNGs rendered
  directly with `dot`. [Graphviz layout documentation](https://www.graphviz.org/docs/layouts/dot/)
- **Mermaid** makes branches easy to spot with colored subgraphs. The text
  renderer wraps long labels, and the Go viewBox is about twice as tall as
  Graphviz's. The Go sample is about 596 KiB. Both PNGs rendered with the CLI
  and Chrome. Setting `htmlLabels: false` made labels visible in a standalone
  SVG rasterizer, which did not display the default HTML labels. The local
  link test used Mermaid's loose security mode with repository inputs.
  GitHub hosts its own renderer and settings, so check the supported version
  before embedding syntax and keep learning links in the surrounding Markdown.
  [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)
  [GitHub diagram documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- **D2** produces clearly separated containers and styled nodes. The Dagre
  sample keeps long labels on a single line and uses more vertical space.
  The Go sample is about 254 KiB. Native PNG succeeded for DSA. Go exceeded
  D2 0.9.0's 32,768-pixel frame height limit with Dagre (47,516 pixels) and
  ELK (34,416 pixels). Rasterizing the full SVG at a smaller size worked.
  [D2 layout engines](https://d2lang.com/tour/layouts/)
  [D2 exports](https://www.d2lang.com/tour/exports/)

The three rendered SVGs for Go preserve both incoming edges to MySQL. The
grouping separates topics, but it does not make a graph of this size readable
as a single inline image. Subject diagrams are a better fit for inline use.

## Reproduce

The samples were rendered with Graphviz 16.1.1, Mermaid CLI 12.2.0, and D2 0.9.0.
Install Graphviz and D2, and use Node.js with the Mermaid CLI. Puppeteer can use
its downloaded Chromium or an installed Chrome via `PUPPETEER_EXECUTABLE_PATH`.
Run these commands from the repository root:

```sh
work=$(mktemp -d)
npm install --prefix "$work/mermaid" @mermaid-js/mermaid-cli@12.2.0
mmdc="$work/mermaid/node_modules/.bin/mmdc"
config=docs/renderer-comparison/mermaid.json

python3 docs/renderer-comparison/generate.py "$work"
for graph in dsa go; do
  dot -Tsvg "$work/$graph.dot" -o "$work/$graph-graphviz.svg"
  dot -Tpng "$work/$graph.dot" -o "$work/$graph-graphviz.png"
  "$mmdc" -c "$config" -i "$work/$graph.mmd" -o "$work/$graph-mermaid.svg"
  "$mmdc" -c "$config" -i "$work/$graph.mmd" -o "$work/$graph-mermaid.png"
  d2 --layout=dagre "$work/$graph.d2" "$work/$graph-d2.svg"
done
d2 --layout=dagre "$work/dsa.d2" "$work/dsa-d2.png"
rsvg-convert --keep-aspect-ratio --height=6000 "$work/go-d2.svg" -o "$work/go-d2.png"
```

The generator emits source files from the current XML. Pin renderer and browser
versions and use the same fonts when comparing output between machines.
Graphviz needs only `dot` on the build runner. Mermaid CLI adds Node.js and a
browser, while D2 needs its own binary and an SVG rasterizer for the Go PNG
workaround. Those tools are only needed to rerun this comparison.

A follow-up could generate one small Mermaid diagram from the XML for a
subject's Markdown guide and check the rendered result on GitHub before
adding more diagrams.
