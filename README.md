# Roadmap Core

![Andersen Logo](logo.png)

This project was created by engineers from [Andersen Software Inc](https://andersenlab.com/)
which were motivated by the idea to describe the graphs of the main knowledge/skills
of different types of engineers which in turn provides a way to develop these graphs
by the community and by the approach which engineers prefer.

## Need

In development teams with official mentoring and level assessments it's important to have a shared understanding of the process. To handle it, teams usually create knowledge roadmaps if form of spreadsheet with subjects and skills for a particular stack, and store it in a cloud.
The issue here is that every developer, regardless of the programming language he uses, has to cover common subject areas, such as computer science, databases, etc. For 10+ stacks changing one skill in a common subject area means you have to manually edit 10+ spreadsheets. That prompts loss of uniformity of content and structure. For developers, who are used to a well-established change process, it discourages further collaboration and improvement of the roadmaps.

## Vision

For developers, Skill Matrix is a module that allows to create and collaborate on knowledge roadmaps. A roadmap is compiled from several subject areas, which are described in separate XML files. This allows to reuse components and to populate a change made in one subject into all roadmaps using it.
Skill Matrix allows to compile a roadmap in a XML syntax, visualize it in form of graph, and convert it to Markdown file and spreadsheet, thus covering all desirable representation formats. As a git project, it establishes an adaptable process for change and collaboration.

## Scope of Initial Release

### Skill Matrix includes

- A collection of Subject Roadmaps, described in custom XMLgraph notation.
- A collection of learning Materials for subjects, described in XMLgraph notation.
- A collection of Stack Roadmaps, which specify relevant subjects for the stacks:
  - [Go](#golang)
  - [Java](#java)
  - [Ruby](#ruby)
  - [PHP](#php)

### A collection of Tools

- [xmlg2dot](tools/xmlg2dot.py) is a tool for converting Roadmap.xml files to DOT syntax. Uses xmlgraph.py
- [xmlg2md](tools/xmlg2md.py) is a tool for converting Materials.xml files to DOT syntax. Uses xmlgraph.py and materials.py
- [Makefile](Makefile) is a major tool that generates Stack Roadmaps and saves them as PNG, SVG, DOT and generated Materials maps and saves them as MD. Uses all tools above.
- [xmlgraph.py](tools/xmlgraph.py) is a library for parsing Roadmap files
- [materials.py](tools/materials.py) is a library for parsing Materials files

## Scope of Future Releases

For future development of the project the following options are considered:
Elaboration on roadmaps structure, adding learning materials.
Creating a tool to check errors in files, such as invalid links in materials files.
Creating roadmaps for other stacks: Python, Ruby, Java Script, .NET C#, Scala, etc.
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

## For developers

### Prerequisites

Before you continue, ensure you meet the following requirements:

- You have installed the latest version of [Python 3](https://www.python.org/downloads/)
- You also have installed [Graphviz](https://www.graphviz.org/download/)
- And you have a basic understanding of graph theory

### Work

All changes should be developed in your own feature branch and merge throw the merge request.
Also, you should update the project each time you change any XML file by:

```bash
make all
```

## Links

- [Programmer Competency Matrix](http://sijinjoseph.com/programmer-competency-matrix/)
- [Roadmaps for Developers: Backend Developer](https://roadmap.sh/backend)
- [Roadmap to becoming a Software Engineer 2018 Edition with Industry Insights: Back-end Roadmap](https://github.com/fauzanbaig/software-engineer-roadmap#-back-end-roadmap)
