# Roadmap Core

This project was created by engineers which were motivated by the idea to describe the graphs of the main knowledge/skills
of different types of engineers which in turn provides a way to develop these graphs
by the community and by the approach which engineers prefer.

## Need

In development teams with official mentoring and level assessments it's important to have a shared understanding of the process. To handle it, teams usually create knowledge roadmaps if form of spreadsheet with subjects and skills for a particular stack, and store it in a cloud.
The issue here is that every developer, regardless of the programming language he uses, has to cover common subject areas, such as computer science, databases, etc. For 10+ stacks changing one skill in a common subject area means you have to manually edit 10+ spreadsheets. That prompts loss of uniformity of content and structure. For developers, who are used to a well-established change process, it discourages further collaboration and improvement of the roadmaps.

## Vision

Roadmap Core helps developers create and collaborate on knowledge roadmaps. Each stack combines subject areas stored in separate XML files. A change to a shared subject flows into every stack that includes it.
The build renders the assembled graph as SVG, PNG, and DOT, and produces a Markdown guide with learning resources.

## Scope of Initial Release

### Roadmap Core includes

- A collection of Subject Roadmaps, described in custom XMLgraph notation.
- A collection of learning Materials for subjects, described in XMLgraph notation.
- A collection of Stack Roadmaps, which specify relevant subjects for the stacks:
  - [Go](#golang)
  - [Java](#java)
  - [Ruby](#ruby)
  - [PHP](#php)
  - [Python](#python)
  - [Computer Science](#computer-science)

### A collection of Tools

- [xmlg2dot](tools/xmlg2dot.py) is a tool for converting Roadmap.xml files to DOT syntax. Uses xmlgraph.py
- [xmlg2md](tools/xmlg2md.py) combines a roadmap and its materials into Markdown.
- [Makefile](Makefile) is a major tool that generates Stack Roadmaps and saves them as PNG, SVG, DOT and generated Materials maps and saves them as MD. Uses all tools above.
- [xmlgraph.py](tools/xmlgraph.py) is a library for parsing Roadmap files
- [materials.py](tools/materials.py) is a library for parsing Materials files
- [Renderer comparison](docs/renderer-comparison/README.md) evaluates Graphviz, Mermaid, and D2 on this project's XML.

## Scope of Future Releases

For future development of the project the following options are considered:
Elaboration on roadmaps structure, adding learning materials.
Creating a tool to check errors in files, such as invalid links in materials files.
Creating roadmaps for other stacks such as JavaScript, .NET, and Scala.
Adding sets of interview questions for subjects and skills (similar to materials).

## Roadmaps

### Golang

- [SVG](stacks/go/data/roadmap.svg) and [PNG](stacks/go/data/roadmap.png) maps
- [Materials](stacks/go/data/roadmap.md)
- [DOT](stacks/go/data/roadmap.dot) version
- [XML](stacks/go/roadmap.xml)

### Java

- [SVG](stacks/java/data/roadmap.svg) and [PNG](stacks/java/data/roadmap.png) maps
- [Materials](stacks/java/data/roadmap.md)
- [DOT](stacks/java/data/roadmap.dot) version
- [XML](stacks/java/roadmap.xml)

### Ruby

- [SVG](stacks/ruby/data/roadmap.svg) and [PNG](stacks/ruby/data/roadmap.png) maps
- [Materials](stacks/ruby/data/roadmap.md)
- [DOT](stacks/ruby/data/roadmap.dot) version
- [XML](stacks/ruby/roadmap.xml)

### PHP

- [SVG](stacks/php/data/roadmap.svg) and [PNG](stacks/php/data/roadmap.png) maps
- [Materials](stacks/php/data/roadmap.md)
- [DOT](stacks/php/data/roadmap.dot) version
- [XML](stacks/php/roadmap.xml)

### Python

- [SVG](stacks/python/data/roadmap.svg) and [PNG](stacks/python/data/roadmap.png) maps
- [Materials](stacks/python/data/roadmap.md)
- [DOT](stacks/python/data/roadmap.dot) version
- [XML](stacks/python/roadmap.xml)

### Computer Science

- [SVG](stacks/cs/data/roadmap.svg) and [PNG](stacks/cs/data/roadmap.png) maps
- [Materials](stacks/cs/data/roadmap.md)
- [DOT](stacks/cs/data/roadmap.dot) version
- [XML](stacks/cs/roadmap.xml)

## For developers

### Prerequisites

Before you continue, ensure you meet the following requirements:

- You have installed the latest version of [Python 3](https://www.python.org/downloads/)
- You also have installed [Graphviz](https://www.graphviz.org/download/)
- And you have a basic understanding of graph theory

### Work

Develop changes on a feature branch and merge them through a pull request.
Resolve XML include paths relative to the file that declares them. After editing XML, rebuild the affected outputs with:

```bash
make all
```

Run `make go` to build only Go. Use `make clean && make all` to remove and
regenerate all checked-in roadmap outputs.

### Validation and tests

Install Python 3, Graphviz, Make, and `xmllint` (`libxml2-utils` on Ubuntu), then run:

```bash
make check
make test
```

`make check` validates the XML schemas, assembled graphs, and material tags.
`make test` also rebuilds every stack in a temporary directory and checks the DOT,
SVG, PNG, and Markdown outputs. GitHub Actions runs both commands on pushes and
pull requests.

## Links

- [Programmer Competency Matrix](http://sijinjoseph.com/programmer-competency-matrix/)
- [Roadmaps for Developers: Backend Developer](https://roadmap.sh/backend)
- [Roadmap to becoming a Software Engineer 2018 Edition with Industry Insights: Back-end Roadmap](https://github.com/fauzanbaig/software-engineer-roadmap#-back-end-roadmap)
