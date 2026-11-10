# Roadmap Core

Roadmap Core is a collection of software engineering knowledge maps and learning resources, maintained as code. It combines reusable subject graphs into roadmaps for Go, Java, PHP, Python, Ruby, and Computer Science, then generates diagrams and Markdown guides.

The project helps developers plan their learning and gives mentors and teams a shared reference for discussing skills. Common subjects—such as databases, networking, and operating systems—live in one place. Updating a shared subject and rebuilding updates every roadmap that includes it, so teams can review changes through Git and pull requests.

## Explore the roadmaps

Open a diagram to browse the topics, or a learning guide to find resources attached to them. Generated files are included in the repository; no installation is needed to read them.

| Roadmap | Diagram | Learning guide | Source |
| --- | --- | --- | --- |
| Go | [SVG](stacks/go/data/roadmap.svg) · [PNG](stacks/go/data/roadmap.png) | [Materials](stacks/go/data/roadmap.md) | [XML](stacks/go/roadmap.xml) · [DOT](stacks/go/data/roadmap.dot) |
| Java | [SVG](stacks/java/data/roadmap.svg) · [PNG](stacks/java/data/roadmap.png) | [Materials](stacks/java/data/roadmap.md) | [XML](stacks/java/roadmap.xml) · [DOT](stacks/java/data/roadmap.dot) |
| PHP | [SVG](stacks/php/data/roadmap.svg) · [PNG](stacks/php/data/roadmap.png) | [Materials](stacks/php/data/roadmap.md) | [XML](stacks/php/roadmap.xml) · [DOT](stacks/php/data/roadmap.dot) |
| Python | [SVG](stacks/python/data/roadmap.svg) · [PNG](stacks/python/data/roadmap.png) | [Materials](stacks/python/data/roadmap.md) | [XML](stacks/python/roadmap.xml) · [DOT](stacks/python/data/roadmap.dot) |
| Ruby | [SVG](stacks/ruby/data/roadmap.svg) · [PNG](stacks/ruby/data/roadmap.png) | [Materials](stacks/ruby/data/roadmap.md) | [XML](stacks/ruby/roadmap.xml) · [DOT](stacks/ruby/data/roadmap.dot) |
| Computer Science (DSA) | [SVG](stacks/cs/data/roadmap.svg) · [PNG](stacks/cs/data/roadmap.png) | [Materials](stacks/cs/data/roadmap.md) | [XML](stacks/cs/roadmap.xml) · [DOT](stacks/cs/data/roadmap.dot) |

The Computer Science stack currently covers data structures and algorithms. The language stacks combine language-specific topics with shared engineering subjects. Learning resources include books, articles, courses, and videos; coverage and resource languages vary by topic.

## How it works

Each subject defines topics and their connections in `roadmap.xml`, plus learning resources in `materials.xml`. Resource tags refer to topic IDs. A stack includes the subjects it needs and connects them beneath its root topic.

The Python tools assemble these XML files into a graph and generate:

- **DOT**, the graph description used by Graphviz.
- **SVG and PNG**, diagrams rendered by Graphviz.
- **Markdown**, a topic outline with links to learning resources.

```text
subjects/<subject>/
  roadmap.xml       Topics and connections shared across stacks
  materials.xml     Resources tagged with topic IDs
stacks/<stack>/
  roadmap.xml       Subject includes and stack-level connections
  materials.xml     Includes for the stack's learning resources
  data/roadmap.*    Generated DOT, SVG, PNG, and Markdown
tools/             XML schemas, parsers, validation, and build tools
tests/             Automated validation and build tests
```

XML include paths are relative to the file that declares them. For example, the Go stack includes the shared database roadmap using `../../subjects/db/roadmap.xml`.

## Build locally

### Requirements

- Python **3.9 or newer**; the tools use only the standard library.
- Graphviz, with `dot` available on `PATH`.
- GNU Make and a POSIX shell.
- `xmllint` for validation and tests (`libxml2-utils` on Ubuntu).
- Git to clone the repository and contribute changes.

On Ubuntu, install the build and validation dependencies with:

```bash
sudo apt-get update
sudo apt-get install python3 graphviz make libxml2-utils
```

Clone the repository and build all six roadmaps:

```bash
git clone https://github.com/dzyanis/roadmap.git
cd roadmap
make all
```

Outputs are written to `stacks/<stack>/data/`. Builds are incremental: unchanged outputs are skipped, and missing outputs are regenerated. Shared subject changes trigger rebuilds across stacks.

To build one stack, use `make go`, `make java`, `make php`, `make python`, `make ruby`, or `make cs`. `make golang` is an alias for `make go`.

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

`make test` runs the automated tests, including building every stack in a temporary directory and checking the generated DOT, SVG, PNG, and Markdown. GitHub Actions runs both commands on pushes and pull requests.

## Contribute

Contributions can improve topic coverage, correct connections, add learning resources, or improve the build tools.

1. Create a feature branch, or fork the repository if you do not have write access.
2. Edit the relevant files in `subjects/`. For stack-specific composition changes, edit the includes and connections in `stacks/`.
3. Keep node and edge IDs unique within each assembled roadmap, keep the graph acyclic, and use existing topic IDs in material tags. When adding a subject to a stack, include its roadmap and materials and connect it to the stack's graph.
4. Run `make check`, `make test`, and `make all`. Inspect the affected diagrams and learning guides.
5. Commit the XML or tool changes together with any updated files in `stacks/*/data/`, then open a pull request explaining the change.

Generated files are committed so readers can browse roadmaps directly on GitHub. Edit their XML sources and regenerate them to keep diagrams and guides consistent.

## Tools and design notes

- [XML graph parser](tools/xmlgraph.py) and [materials parser](tools/materials.py): load and combine source files.
- [DOT converter](tools/xmlg2dot.py) and [Markdown converter](tools/xmlg2md.py): generate graph descriptions and learning guides.
- [Validator](tools/validate.py), [graph schema](tools/xmlgraph.xsd), and [materials schema](tools/materials.xsd): define and check the input format.
- [Makefile](Makefile) and [build script](tools/build.sh): coordinate generation of all four output formats.
- [Renderer comparison](docs/renderer-comparison/README.md): evaluates Graphviz, Mermaid, and D2 using this project's graphs. Graphviz remains the renderer used by the build.
