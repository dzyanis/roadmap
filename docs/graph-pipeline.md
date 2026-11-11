# Shared graph pipeline and JSON contract

XML remains the only manually maintained source of topics, relationships, and
resources. `make all` produces `graph.json` alongside each roadmap's existing
DOT, SVG, PNG, and Markdown files in `generated/<category>/<name>/`.

```text
XML includes → XSD validation → endpoint/cycle/resource checks → pipeline.Graph
                                                               ├─ graph.json
                                                               ├─ roadmap.dot → SVG/PNG
                                                               └─ guide.md
```

`tools/pipeline.py:load_roadmap` resolves includes relative to their declaring
file, validates every included file (even fragments with arbitrary filenames),
assembles the graph, checks the requested root and material tags, and attaches
resources and subject membership to topics. No exporter reopens XML. The build
calls the loader once through `tools/export.py`; all three data exporters receive
that same model. Graphviz reads the resulting DOT.

Duplicate topic/edge IDs, missing endpoints, graph/include cycles, unknown roots,
unknown material tags, missing files, and schema violations fail before exports
begin. Build outputs are staged; validation, export, or rendering failure leaves
previous published files untouched. Files are moved into place only after all
generation succeeds. Publication is a sequence of file moves, not a transactional
directory swap. `make check` also validates standalone subjects not used by any
roadmap. `xmllint` is required for both checks and builds.

## Exporter interface

```python
from pipeline import load_roadmap
from graphjson import write_json

graph = load_roadmap(
    'roadmaps/roles/go-engineer/roadmap.xml',
    'roadmaps/roles/go-engineer/materials.xml',
    rootid='backend',
)
with open('graph.json', 'w', encoding='utf-8', newline='\n') as output:
    write_json(graph, output)
```

Run with `tools/` on Python's import path. The model provides:

| Field | Meaning |
| --- | --- |
| `graph.id` | Roadmap key, normally `category/directory-name`; override with `roadmap_id` for external sources. |
| `graph.root` | Requested root topic ID. Optional only for graph-only tools. |
| `graph.nodes` | ID → topic, in XML/include encounter order. |
| `topic.id`, `topic.label` | Original XML values, without slugifying or renumbering. |
| `topic.childrenids` | Outgoing containment targets in XML edge order, including shared descendants. |
| `topic.subjects` | Tuple of subject directory IDs derived from the topic's declaring file. |
| `topic.resources` | Tuple of resolved resources, in XML/include/tag encounter order. |
| `graph.edges` | ID → edge with `id`, `source`, `target`, and `type`, in XML/include encounter order. |
| `graph.subjects` | Sorted tuple of subject IDs represented by topics. |

Treat the assembled model as read-only. Resources expose `type`, `title`, `url`,
`language`, `description`, `translate_lang`, and `translate_url`. Internal source
paths retained by the low-level parsers are diagnostic data, never JSON fields.

To add an exporter, implement `write_format(graph, output)` using the model, then
register it in `tools/export.py` and add its filename to `tools/build.sh` and the
Makefile's `outputs`. Iterate `graph.edges` to preserve multiple incoming edges;
do not flatten the graph into a single-parent tree. Keep layout, coordinates,
colors, clustering, and renderer identifiers in the exporter. The existing
renderer comparison in `docs/renderer-comparison/generate.py` now uses this same
loader; independent renderer experiments remain tracked in #40.

DOT and Markdown retain their previous ordering and formatting. Markdown is a
rooted outline: it repeats shared descendants under each incoming path and
omits topics unreachable from the root, as before. DOT and JSON include every
topic and edge, including disconnected components. Legacy `xmlg2dot.py` and
`xmlg2md.py` commands remain available; the graph-only DOT command does not load
materials. Subject-only prototypes may omit the root. JSON/Markdown require one.

## JSON version 1

The machine-readable contract is [graph-v1.schema.json](../schemas/graph-v1.schema.json).
`schema_version` is an integer; consumers must reject unsupported versions.
Changes to required fields, field meanings, ID rules, or supported edge types
require a new contract version. Generated JSON is UTF-8, two-space indented,
with a trailing newline. It contains no timestamps, absolute paths, or layout
fields. Identical XML trees in different checkout locations produce identical
bytes. Topics, edges, and subject IDs are sorted lexically by their IDs. Resource
arrays retain source order, including duplicates; JSON ordering is not a learning
sequence. DOT/Markdown continue to use XML ordering.

| JSON field | Contract |
| --- | --- |
| `schema_version` | `1`. |
| `roadmap.id` | Stable public roadmap key such as `roles/go-engineer`. |
| `roadmap.label` | Root topic's label, suitable for a roadmap selector. |
| `roadmap.root` | ID of a topic in `topics`. Existing roadmap roots remain `backend`. |
| `subjects` | Sorted unique subject directory names represented in the roadmap. |
| `topics[]` | Objects with `id`, `label`, `subjects`, and `resources`. |
| `topics[].subjects` | Declaring subject directory ID, including nested fragments; empty for topics declared in the roadmap itself. This is provenance, not inferred ancestry. |
| `topics[].resources[]` | `type`, `title`, `url`, `language`, `description`, `translation`. Resources tagged to several topics appear under each. |
| `translation` | `null`, or an object containing `language` and `url`. |
| `edges[]` | Objects with original XML `id`, `source`, `target`, and `type: "contains"`. Every endpoint references an exported topic. |

Topic and edge IDs are unique within a roadmap, not across roadmaps. A topic's
identity for website state is `(roadmap.id, topic.id)`. A viewer can use links
such as `?roadmap=roles%2Fgo-engineer&topic=os_processes`, encoding each component;
this is a consumer routing example, not a URL generated by the model. A selector
can use each graph's `roadmap` metadata. Search indexes topic labels and resource
titles; details read the selected topic and its resources. The website's catalog,
route handling, and rendering choice remain in #39.

Resource titles and descriptions collapse whitespace; URLs strip line-break
indentation as the existing materials parser does. Missing descriptions are empty
strings. Existing behavior skips resources with empty titles or URLs and ignores
empty tags. The XSD still requires the title, URL, tags, and language fields.
JSON strings are data: HTML consumers must escape text and apply their URL policy
when rendering links.

## Relationship semantics and planned extension

Existing untyped XML edges are **contains**: `source` is the broader parent topic,
`target` is an included subtopic. They express the current learning outline, not
a claim that the source must be learned first. Shared descendants and parallel
edges with distinct IDs remain valid. All current edges must be acyclic.

The following extension is deliberately separate from this compatibility refactor:

| Type | Direction and meaning | Cycle rule |
| --- | --- | --- |
| `contains` | Broader topic → contained subtopic. Legacy edges default to this type. | Reject cycles in the containment subgraph. |
| `prerequisite` | Required topic → topic that depends on it. | Reject cycles in the prerequisite subgraph. |
| `related-to` | Symmetric association; source/target record the declaration, not ordering. | Cycles allowed. |

The follow-up must add an optional XML edge `type`, reject unknown types, validate
each directed type independently, and retain all edges in the model. A mixed
contains/prerequisite cycle is not itself a same-type cycle; cross-type policy
must be explicit rather than applying a blanket DAG check. Markdown must traverse
only containment edges; other relations need a separate presentation. Related
edges must never enter recursive outline traversal. Tests must cover valid related
cycles, invalid containment/prerequisite cycles, mixed-type cycles, and legacy XML.
The JSON version must advance before exposing richer edge types. Implementation
is tracked in [#46](https://github.com/dzyanis/roadmap/issues/46).
