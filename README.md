# Roadmap Core

Roadmap Core is a collection of software engineering knowledge maps and learning resources, maintained as code. It combines reusable subject graphs into roadmaps for Go Engineer, Java Engineer, PHP Engineer, Python Engineer, Ruby Engineer, DevOps Engineer, and Data Structures and Algorithms, then generates diagrams and Markdown guides.

The project helps developers plan their learning and gives mentors and teams a shared reference for discussing skills. Common subjects—such as databases, networking, and operating systems—live in one place. Updating a shared subject and rebuilding updates every roadmap that includes it, so teams can review changes through Git and pull requests.

## Explore the roadmaps

Open a diagram to browse the topics, or a learning guide to find resources attached to them. Generated files are included in the repository; no installation is needed to read them.

| Roadmap | Diagram | Learning guide | Source |
| --- | --- | --- | --- |
| Go Engineer | [SVG](generated/roles/go-engineer/roadmap.svg) · [PNG](generated/roles/go-engineer/roadmap.png) | [Materials](generated/roles/go-engineer/guide.md) | [XML](roadmaps/roles/go-engineer/roadmap.xml) · [DOT](generated/roles/go-engineer/roadmap.dot) |
| Java Engineer | [SVG](generated/roles/java-engineer/roadmap.svg) · [PNG](generated/roles/java-engineer/roadmap.png) | [Materials](generated/roles/java-engineer/guide.md) | [XML](roadmaps/roles/java-engineer/roadmap.xml) · [DOT](generated/roles/java-engineer/roadmap.dot) |
| PHP Engineer | [SVG](generated/roles/php-engineer/roadmap.svg) · [PNG](generated/roles/php-engineer/roadmap.png) | [Materials](generated/roles/php-engineer/guide.md) | [XML](roadmaps/roles/php-engineer/roadmap.xml) · [DOT](generated/roles/php-engineer/roadmap.dot) |
| Python Engineer | [SVG](generated/roles/python-engineer/roadmap.svg) · [PNG](generated/roles/python-engineer/roadmap.png) | [Materials](generated/roles/python-engineer/guide.md) | [XML](roadmaps/roles/python-engineer/roadmap.xml) · [DOT](generated/roles/python-engineer/roadmap.dot) |
| Ruby Engineer | [SVG](generated/roles/ruby-engineer/roadmap.svg) · [PNG](generated/roles/ruby-engineer/roadmap.png) | [Materials](generated/roles/ruby-engineer/guide.md) | [XML](roadmaps/roles/ruby-engineer/roadmap.xml) · [DOT](generated/roles/ruby-engineer/roadmap.dot) |
| DevOps Engineer | [SVG](generated/roles/devops-engineer/roadmap.svg) · [PNG](generated/roles/devops-engineer/roadmap.png) | [Materials](generated/roles/devops-engineer/guide.md) | [XML](roadmaps/roles/devops-engineer/roadmap.xml) · [DOT](generated/roles/devops-engineer/roadmap.dot) |
| Data Structures and Algorithms | [SVG](generated/foundations/data-structures-algorithms/roadmap.svg) · [PNG](generated/foundations/data-structures-algorithms/roadmap.png) | [Materials](generated/foundations/data-structures-algorithms/guide.md) | [XML](roadmaps/foundations/data-structures-algorithms/roadmap.xml) · [DOT](generated/foundations/data-structures-algorithms/roadmap.dot) |

The foundation roadmap covers data structures and algorithms, not a complete Computer Science curriculum. The engineer roadmaps combine language-specific topics with shared engineering subjects. The DevOps Engineer roadmap combines operating systems, networking, databases, and development processes with automation, containers, infrastructure as code, delivery pipelines, cloud infrastructure, observability, reliability, and security. Learning resources include books, articles, courses, and videos; coverage and resource languages vary by topic.

## How it works

Each subject defines topics and their connections in `roadmap.xml`, plus learning resources in `materials.xml`. Resource tags refer to topic IDs. A roadmap includes the subjects it needs and connects them beneath its root topic.

The Python tools validate and assemble these XML files into one shared graph and generate:

- **DOT**, the graph description used by Graphviz.
- **SVG and PNG**, diagrams rendered by Graphviz.
- **Markdown**, a topic outline with links to learning resources.
- **JSON**, versioned website data with stable topic IDs, edges, subjects, and resources.

```text
subjects/<subject>/                   Reusable knowledge and resources
  roadmap.xml
  materials.xml
roadmaps/<category>/<name>/           Curated learning paths
  roadmap.xml                        Topic includes and root connections
  materials.xml                      Resource includes
schemas/                             XML schemas
generated/<category>/<name>/          Generated, committed outputs
  roadmap.dot / roadmap.svg / roadmap.png
  guide.md
  graph.json
tools/                               XML loading, validation, and exporters
tests/                               Validation and build tests
```

XML include paths are relative to the file that declares them. For example, the Go Engineer roadmap includes databases using `../../../subjects/databases/roadmap.xml`. Categories are `roles`, `technologies`, and `foundations`. Subjects define reusable knowledge; roadmaps combine subjects into learning paths. See the [layout and migration guide](docs/layout-migration.md).

## Build locally

### Requirements

- Python **3.9 or newer**; the tools use only the standard library.
- Graphviz, with `dot` available on `PATH`.
- GNU Make and a POSIX shell.
- `xmllint` for validation, builds, and tests (`libxml2-utils` on Ubuntu).
- Git to clone the repository and contribute changes.

On Ubuntu, install the build and validation dependencies with:

```bash
sudo apt-get update
sudo apt-get install python3 graphviz make libxml2-utils
```

Clone the repository and build all seven roadmaps:

```bash
git clone https://github.com/dzyanis/roadmap.git
cd roadmap
make all
```

Outputs are written to `generated/<category>/<name>/`. Builds are incremental: unchanged outputs are skipped, and missing outputs are regenerated. Shared subject changes trigger rebuilds across roadmaps.

To build one roadmap, use `make go-engineer`, `make java-engineer`, `make php-engineer`, `make python-engineer`, `make ruby-engineer`, `make devops-engineer`, or `make data-structures-algorithms`. Legacy commands `make go`, `make golang`, `make java`, `make php`, `make python`, `make ruby`, `make devops`, and `make cs` remain aliases. Category-qualified targets such as `make roles/go-engineer` are also supported.

To remove the generated outputs and rebuild everything:

```bash
make clean && make all
```

### Validate and test

```bash
make check
make test
```

`make check` validates the XML against the schemas and checks assembled graphs for duplicate IDs, missing edge endpoints, cycles, and material tags that do not match a topic. It checks structure and references within the roadmaps; it does not check whether external resource URLs are still available.

`make test` runs the automated tests, including building every roadmap in a temporary directory and checking the generated DOT, SVG, PNG, Markdown, and JSON. GitHub Actions runs both commands on pushes and pull requests. Builds validate included XML and resource references before publishing any outputs.

## Contribute

Contributions can improve topic coverage, correct connections, add learning resources, or improve the build tools.

1. Create a feature branch, or fork the repository if you do not have write access.
2. Edit the relevant files in `subjects/`. For roadmap composition changes, edit the includes and connections in `roadmaps/`.
3. Keep node and edge IDs unique within each assembled roadmap, keep the graph acyclic, and use existing topic IDs in material tags. When adding a subject to a roadmap, include its roadmap and materials and connect it to the roadmap's graph.
4. Run `make check`, `make test`, and `make all`. Inspect the affected diagrams and learning guides.
5. Commit the XML or tool changes together with any updated files in `generated/`, then open a pull request explaining the change.

Generated files are committed so readers can browse roadmaps directly on GitHub. Edit their XML sources and regenerate them to keep diagrams and guides consistent.

## Tools and design notes

- [XML graph parser](tools/xmlgraph.py) and [materials parser](tools/materials.py): load and combine source files.
- [Shared graph loader](tools/pipeline.py), [JSON schema](schemas/graph-v1.schema.json), and [pipeline/exporter guide](docs/graph-pipeline.md): define the validated model, versioned JSON contract, and how to add exporters.
- [DOT converter](tools/xmlg2dot.py) and [Markdown converter](tools/xmlg2md.py): generate graph descriptions and learning guides.
- [Validator](tools/validate.py), [graph schema](schemas/roadmap.xsd), and [materials schema](schemas/materials.xsd): define and check the input format.
- [Makefile](Makefile), [export driver](tools/export.py), and [build script](tools/build.sh): coordinate generation of all five output formats from one assembled model.
- [Renderer comparison](docs/renderer-comparison/README.md): evaluates Graphviz, Mermaid, and D2 using this project's graphs. Graphviz remains the renderer used by the build.
