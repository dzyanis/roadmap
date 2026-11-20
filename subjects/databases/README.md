# Database subject

The learning outline starts with modeling, SQL, indexes and transactions, then
covers distributed data, operations and application access. Data models and
products form a separate reference branch; transactional and analytical workloads
explain OLTP/OLAP and column-oriented storage. Search and messaging remain
explicitly adjacent systems so existing role roadmaps retain their coverage.

All 34 original topic IDs remain stable, including historical spellings such as
`db_search_elasticseaerch` and `db_nosql_colbase`. Display labels and containment
have changed: the latter now means column-oriented analytical storage, outside
NoSQL. Edge IDs were regenerated from their endpoints. MySQL remains a shared
node, appearing as both a relational database and an OLTP example; these are
examples, not exclusive classifications of product capabilities. Containment
edges describe the outline, not prerequisite relationships.

The subject contains 71 topics and 37 learning resources. Free readings cover
every major branch. PostgreSQL supplies most practical relational examples;
Cassandra, Redis, MongoDB and ClickHouse illustrate other models and workloads.
The two older SQL/Oracle books are supplementary and explicitly versioned.
Kubernetes in Action belongs to `subjects/software-development/materials.xml`.

The initial scope favors application fundamentals and operational literacy.
Detailed vendor administration, distributed consensus proofs, specialized index
families, and exhaustive product catalogs remain further study. Search and
messaging receive introductory resources, not full independent curricula.

Resource URLs were checked during implementation of #36. Publisher book pages
are listings, not free books. O'Reilly and RabbitMQ reject the local HTTP probe
with 403; both pages were also inspected through web retrieval. Availability
checks do not guarantee future availability or validate every example in a book.
The historical renderer comparison under `docs/prototypes/mermaid` retains its
recorded input snapshot; current production graphs are under `generated/`.
