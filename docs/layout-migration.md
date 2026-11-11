# Roadmap layout and migration

Roadmaps are curated learning paths; subjects are reusable bodies of knowledge.
A role roadmap prepares for a profession, a technology roadmap teaches a tool or
platform, and a foundation roadmap covers knowledge shared across roles.

## Source and output locations

| Previous roadmap | Source directory | Generated directory | Display name |
| --- | --- | --- | --- |
| `stacks/go` | `roadmaps/roles/go-engineer` | `generated/roles/go-engineer` | Go Engineer |
| `stacks/java` | `roadmaps/roles/java-engineer` | `generated/roles/java-engineer` | Java Engineer |
| `stacks/php` | `roadmaps/roles/php-engineer` | `generated/roles/php-engineer` | PHP Engineer |
| `stacks/python` | `roadmaps/roles/python-engineer` | `generated/roles/python-engineer` | Python Engineer |
| `stacks/ruby` | `roadmaps/roles/ruby-engineer` | `generated/roles/ruby-engineer` | Ruby Engineer |
| `stacks/devops` | `roadmaps/roles/devops-engineer` | `generated/roles/devops-engineer` | DevOps Engineer |
| `stacks/cs` | `roadmaps/foundations/data-structures-algorithms` | `generated/foundations/data-structures-algorithms` | Data Structures and Algorithms |

Each source directory contains `roadmap.xml` and `materials.xml`. Each generated
directory contains `roadmap.dot`, `roadmap.svg`, `roadmap.png`, and `guide.md`.
Generated outputs remain committed and must be rebuilt, never edited manually.
The build stamp `.roadmap-built` is ignored by Git.

The old Computer Science roadmap only composed DSA topics, so its new name states
that scope explicitly. The reusable `subjects/computer-science` subject still
contains broader computing topics used by role roadmaps.

| Old subject directory | New subject directory |
| --- | --- |
| `subjects/os` | `subjects/operating-systems` |
| `subjects/net` | `subjects/networking` |
| `subjects/db` | `subjects/databases` |
| `subjects/dev` | `subjects/software-development` |
| `subjects/dsa` | `subjects/data-structures-algorithms` |
| `subjects/cs` | `subjects/computer-science` |

XML schemas now live in `schemas/roadmap.xsd` and `schemas/materials.xsd`.
Topic IDs, edge IDs, material tags, and graph relationships are preserved. Only
roadmap root display labels change. The existing root ID `backend` is retained
for compatibility; it is not the name of a profession.

## Building and compatibility

Run `make all`, `make check`, and `make test` as before. New individual targets
are the roadmap directory names, such as `make go-engineer` or
`make data-structures-algorithms`. Category-qualified targets such as
`make roles/go-engineer` are available when an explicit category is useful.
New roadmap names should be globally unique to keep short build targets clear.

Legacy targets `go`, `golang`, `java`, `php`, `python`, `ruby`, `devops`, and `cs`
remain aliases. The low-level script now accepts a category-qualified key, for
example `sh tools/build.sh roles/go-engineer`. Make handles incremental builds;
the script always regenerates that roadmap.

Old GitHub directory links to `stacks/<name>` have navigation READMEs pointing to
the new locations. GitHub does not redirect arbitrary renamed file/raw URLs:
old `stacks/<name>/data/roadmap.*`, source XML, abbreviated subject, and schema
URLs must be updated using the mappings above. Historical commit URLs continue
to identify their original files. Do not maintain duplicate source or generated
files to emulate redirects.

## Planned additions

The initial migration creates only existing content and tooling. As the related
issues are implemented, use these conventions:

- Kubernetes (#41): `subjects/kubernetes` and
  `roadmaps/technologies/kubernetes`, with outputs in
  `generated/technologies/kubernetes`.
- AWS (#43): `subjects/aws` plus reusable architecture knowledge, composed in
  `roadmaps/roles/aws-solutions-architect`.
- Shared pipeline (#42): extend the current Python tools with a common graph
  model and exporters under `tools/exporters`; add the JSON schema under
  `schemas` and `graph.json` beside each roadmap's other generated files.
- Renderer prototypes (#40): consume the shared sources/model and keep
  technology-specific experiments independent of source directory organization.
- HTML site (#39): place viewer source under `site`. Discover roadmaps by
  category and use category/name as the stable roadmap key, with XML root labels
  as display names. Preserve topic IDs for topic links. Navigation should expose
  roles, technologies, and foundations, with names distinct from display labels.

XML remains the source of truth. No placeholder subjects, site implementation,
JSON contract, or new renderer is introduced by the layout migration.
