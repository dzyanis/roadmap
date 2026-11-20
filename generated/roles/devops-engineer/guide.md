# DevOps Engineer

## Operating Systems

- book: [Modern Operating Systems, Fifth Edition](https://www.pearson.com/en-us/subject-catalog/p/modern-operating-systems/P200000003295/9780137618880)
- book: [Operating System Concepts, Tenth Edition](https://os-book.com/OS10/)
- book: [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)


### Kernel and User Space

- article: [OSTEP: Limited Direct Execution](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf)


#### Privilege Levels and System Calls

#### Interrupts, Exceptions, and Timers

### Processes and Threads

- article: [OSTEP: Processes](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf)


#### Thread Lifecycle and Shared Address Space

#### CPU Scheduling and Context Switching

#### Concurrency and Parallelism

- article: [OSTEP: Concurrency and Threads](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf)


##### Locks, Semaphores, and Condition Variables

##### Race Conditions and Deadlocks

#### Process Creation, Execution, and Exit

#### IPC: Pipes, Shared Memory, and Message Queues

#### Signals and Process Termination

### Memory Management

- article: [OSTEP: Address Spaces](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf)


#### Virtual Memory

##### Address Spaces and Memory Mapping

##### Paging, Page Faults, and Swapping

##### Page Tables and Translation Lookaside Buffers

#### Allocation: Stack and Heap

### File Systems and Persistence

- video: [Files and File Systems: Crash Course Computer Science #20](https://www.youtube.com/watch?v=KN8YgJnShPM)
- article: [OSTEP: Files and Directories](https://pages.cs.wisc.edu/~remzi/OSTEP/file-intro.pdf)


#### Files, Directories, Mounts, and Links

#### File Ownership and Permissions

#### Writeback, Journaling, and Crash Recovery

### Input and Output

- article: [OSTEP: I/O Devices](https://pages.cs.wisc.edu/~remzi/OSTEP/file-devices.pdf)


#### File Descriptors and Device I/O

#### Buffering and Caching

#### Blocking, Nonblocking I/O, and Readiness

### Protection and Access Control

- article: [OSTEP: Access Control](https://pages.cs.wisc.edu/~remzi/OSTEP/security-access.pdf)


#### Users, Groups, and Least Privilege

#### Process Isolation and Access Checks

### Virtualization

- article: [QEMU System Emulation Introduction](https://www.qemu.org/docs/master/system/introduction.html)


#### OS-Level Virtualization and Containers

- article: [Docker: What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)


##### Linux Namespaces

- article: [Linux namespaces manual](https://man7.org/linux/man-pages/man7/namespaces.7.html)


##### Linux Control Groups

- article: [Linux kernel: Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)


##### Docker

- book: [Docker in Action, Second Edition](https://www.manning.com/books/docker-in-action-second-edition)
- article: [Docker: What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)


#### Hardware Virtualization and Hypervisors

- article: [QEMU System Emulation Introduction](https://www.qemu.org/docs/master/system/introduction.html)


##### Hosts, Guests, and Virtual Hardware

##### VirtualBox

##### VMware ESXi

### Shells and Command-Line Fundamentals

- article: [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)


#### Quoting, Expansion, and Environment Variables

#### Pipelines and Redirection

#### Exit Status, Signals, and Job Control

#### Bash

- article: [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)


#### Zsh

### Linux Administration and Diagnostics

- article: [systemctl reference](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)


#### Service Lifecycle and Logs (systemd)

- article: [systemctl reference](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)


#### Process and CPU Inspection (ps, top)

#### Memory, Disk Space, and I/O (vmstat, df, du, iostat)

#### System Call Tracing (strace)

### Operating System Characteristics

- book: [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)


#### Workload: Batch Processing

#### Workload: Interactive Time-Sharing

#### Coordination: Distributed Systems

#### Connectivity: Network Operating Systems

#### Timing: Real-Time Guarantees

## Computer Network

- book: [Computer Networks](https://www.amazon.com/Computer-Networks-Tanenbaum-International-Economy/dp/9332518742)


### Open Systems Interconnection model

### gRPC

### REST API

### GraphQL

### SOAP

### DNS

### Protocols

#### IP

#### TCP

#### UDP

#### HTTP

#### TLS

#### SSL

### Websocket

### Authorization and Authentication

#### Authorization

#### Authentication

#### OAuth

#### JWT

#### Cookie

## Databases

- article: [PostgreSQL tutorial: relational concepts and SQL](https://www.postgresql.org/docs/current/tutorial.html)


### Data modeling

- article: [PostgreSQL constraints: keys and relationships](https://www.postgresql.org/docs/current/ddl-constraints.html)


#### Keys, constraints and relationships

- article: [PostgreSQL constraints: keys and relationships](https://www.postgresql.org/docs/current/ddl-constraints.html)


#### Normalization and functional dependencies

- article: [Database normalization basics (Microsoft)](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)


#### Denormalization and read/write tradeoffs

- article: [MongoDB: embedding versus references](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)


### SQL

- book: [SQL Bible (2008; supplementary, older SQL reference)](https://www.wiley-vch.de/en/areas-interest/computing-computer-sciences/sql-bible-978-0-470-22906-4)
- article: [PostgreSQL tutorial: relational concepts and SQL](https://www.postgresql.org/docs/current/tutorial.html)


#### SELECT, filtering and ordering

- article: [PostgreSQL tutorial: relational concepts and SQL](https://www.postgresql.org/docs/current/tutorial.html)


#### Joins and NULL semantics

- article: [PostgreSQL tutorial: relational concepts and SQL](https://www.postgresql.org/docs/current/tutorial.html)


#### Aggregation and GROUP BY

- article: [PostgreSQL tutorial: relational concepts and SQL](https://www.postgresql.org/docs/current/tutorial.html)


#### Subqueries and CTEs

- article: [PostgreSQL table expressions and subqueries](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- article: [PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)


#### Window functions

- article: [PostgreSQL window functions tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)


#### DDL and schema changes

- article: [PostgreSQL constraints: keys and relationships](https://www.postgresql.org/docs/current/ddl-constraints.html)


#### INSERT, UPDATE and DELETE

- article: [PostgreSQL tutorial: relational concepts and SQL](https://www.postgresql.org/docs/current/tutorial.html)


### Indexes and query performance

- article: [PostgreSQL indexes: types, multicolumn indexes and costs](https://www.postgresql.org/docs/current/indexes.html)


#### B-tree indexes and lookup costs

- article: [PostgreSQL indexes: types, multicolumn indexes and costs](https://www.postgresql.org/docs/current/indexes.html)


#### Composite indexes and column order

- article: [PostgreSQL indexes: types, multicolumn indexes and costs](https://www.postgresql.org/docs/current/indexes.html)


#### Selectivity and planner statistics

- article: [PostgreSQL planner statistics](https://www.postgresql.org/docs/current/planner-stats.html)


#### Query plans and EXPLAIN

- article: [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)


#### Index write and storage costs

- article: [PostgreSQL indexes: types, multicolumn indexes and costs](https://www.postgresql.org/docs/current/indexes.html)


### Transactions and concurrency

- article: [PostgreSQL concurrency control](https://www.postgresql.org/docs/current/mvcc.html)


#### ACID guarantees

- article: [PostgreSQL transaction tutorial](https://www.postgresql.org/docs/current/tutorial-transactions.html)


#### Isolation levels and anomalies

- article: [PostgreSQL concurrency control](https://www.postgresql.org/docs/current/mvcc.html)


#### Multiversion concurrency control

- article: [PostgreSQL concurrency control](https://www.postgresql.org/docs/current/mvcc.html)


#### Locking and contention

- article: [PostgreSQL explicit locking and deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html)


#### Deadlocks and transaction retries

- article: [PostgreSQL explicit locking and deadlocks](https://www.postgresql.org/docs/current/explicit-locking.html)
- article: [PostgreSQL serialization failure handling](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html)


### Distributed data

- article: [Cassandra distributed architecture: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)


#### Replication and replication lag

- article: [Cassandra distributed architecture: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)
- article: [PostgreSQL high availability and replication](https://www.postgresql.org/docs/current/high-availability.html)


#### Partitioning and sharding

- article: [Cassandra distributed architecture: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)


#### Consistency and availability tradeoffs

- article: [Cassandra distributed architecture: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)
- article: [Werner Vogels: eventual consistency](https://www.allthingsdistributed.com/2008/12/eventually_consistent.html)


##### CAP under network partitions

- article: [Eric Brewer: CAP twelve years later](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/)


##### BASE and eventual consistency

- article: [Werner Vogels: eventual consistency](https://www.allthingsdistributed.com/2008/12/eventually_consistent.html)


### Operations and recovery

- article: [Flyway versioned migrations](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/versioned-migrations)


#### Versioned migrations and safe rollout

- article: [Flyway versioned migrations](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/versioned-migrations)


#### Backups, point-in-time recovery and restore tests

- article: [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- article: [PostgreSQL continuous archiving and recovery](https://www.postgresql.org/docs/current/continuous-archiving.html)


#### Monitoring queries, capacity and replication

- article: [PostgreSQL monitoring database activity](https://www.postgresql.org/docs/current/monitoring.html)


#### Roles, least privilege and access control

- article: [PostgreSQL database roles](https://www.postgresql.org/docs/current/user-manag.html)


### Application access

- article: [PostgreSQL parameterized query execution](https://www.postgresql.org/docs/current/libpq-exec.html)


#### Parameterized queries and SQL injection prevention

- article: [PostgreSQL parameterized query execution](https://www.postgresql.org/docs/current/libpq-exec.html)


#### Connection pools and connection lifecycle

- article: [PgBouncer connection pooling features](https://www.pgbouncer.org/features.html)


### Data models and representative products

- article: [PostgreSQL object-relational features](https://www.postgresql.org/docs/current/extend.html)


#### Relational databases

- article: [PostgreSQL tutorial: relational concepts and SQL](https://www.postgresql.org/docs/current/tutorial.html)


##### Object-relational features

- article: [PostgreSQL object-relational features](https://www.postgresql.org/docs/current/extend.html)


##### PostgreSQL

- article: [PostgreSQL tutorial: relational concepts and SQL](https://www.postgresql.org/docs/current/tutorial.html)


##### MySQL

##### Oracle

- book: [Oracle PL/SQL Programming (through Oracle 12c; supplementary, version-specific)](https://www.oreilly.com/library/view/oracle-pl-sql-programming/9781449324445/)


##### Firebird

#### Object databases: persistent objects and identity

- article: [ObjectDB: object database concepts](https://www.objectdb.com/database/faq)


#### NoSQL data models

- article: [NOSQL](https://martinfowler.com/nosql.html)
- book: [NoSQL Distilled](https://martinfowler.com/books/nosql.html)


##### Key-value and data-structure stores

- article: [Redis data types](https://redis.io/docs/latest/develop/data-types/)


###### Redis

- article: [Redis data types](https://redis.io/docs/latest/develop/data-types/)


##### Document databases

- article: [MongoDB: embedding versus references](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)


###### MongoDB

- article: [MongoDB: embedding versus references](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)


##### Wide-column databases

- article: [Cassandra distributed architecture: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)


###### Apache Cassandra

- article: [Cassandra distributed architecture: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)


##### Graph databases

- article: [Neo4j graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)


###### Neo4j

- article: [Neo4j graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)


###### OrientDB (multi-model)

##### Time-series databases

- article: [InfluxDB time-series data model](https://docs.influxdata.com/influxdb/v2/reference/key-concepts/data-elements/)


### Transactional and analytical workloads

- article: [ClickHouse: OLAP, OLTP and column-oriented storage](https://clickhouse.com/docs/get-started/about/intro)


#### OLTP: short application transactions

- article: [ClickHouse: OLAP, OLTP and column-oriented storage](https://clickhouse.com/docs/get-started/about/intro)


##### MySQL

#### OLAP: analytical databases

- article: [ClickHouse: OLAP, OLTP and column-oriented storage](https://clickhouse.com/docs/get-started/about/intro)


##### Column-oriented analytical storage

- article: [ClickHouse: OLAP, OLTP and column-oriented storage](https://clickhouse.com/docs/get-started/about/intro)


###### ClickHouse (SQL analytics)

- article: [ClickHouse: OLAP, OLTP and column-oriented storage](https://clickhouse.com/docs/get-started/about/intro)


### Adjacent systems: search and messaging

- article: [Elasticsearch introduction](https://www.elastic.co/docs/products/elasticsearch)


#### Search engines and inverted indexes

- article: [Elasticsearch introduction](https://www.elastic.co/docs/products/elasticsearch)


##### Elasticsearch

- article: [Elasticsearch introduction](https://www.elastic.co/docs/products/elasticsearch)


##### Sphinx

#### Message brokers and delivery semantics

- article: [RabbitMQ queues and delivery semantics](https://www.rabbitmq.com/docs/queues)


##### Kafka

##### RabbitMQ

- article: [RabbitMQ queues and delivery semantics](https://www.rabbitmq.com/docs/queues)


##### Amazon Simple Queue Service

## Software Development Processes

- book: [Working Effectively with Legacy Code](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)
- book: [Refactoring: Improving the Design of Existing Code](https://www.amazon.com/Refactoring-Improving-Design-Existing-Code/dp/0201485672)
- book: [The Pragmatic Programmer: From Journeyman to Master](https://www.amazon.com/Pragmatic-Programmer-Journeyman-Master/dp/020161622X)
- book: [Code Complete: A Practical Handbook of Software Construction](https://www.amazon.com/Code-Complete-Practical-Handbook-Construction/dp/0735619670)
- book: [Clean Code: A Handbook of Agile Software Craftsmanship](https://www.amazon.com/gp/product/0132350882)


### Testing

- book: [Test Driven Development: By Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- article: [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- article: [How deep are your unit tests?](https://stackoverflow.com/questions/153234/how-deep-are-your-unit-tests)


#### Test-driven development

#### Behavior-driven development

### Build Systems

#### Make

#### Maven

- article: [Системы сборки проектов Maven](http://www.apache-maven.ru/)
- article: [Идеальный мавен. Часть 2: структура проекта](https://habr.com/ru/post/344480/)


#### Ant

#### Gradle

- book: [Gradle in Action](http://barbra-coco.dyndns.org/student/Gradle%20in%20Action.pdf)


### Bug tracking systems

#### Jira

#### Redmine

#### TFS

### Version Control

- article: [4 книги о системах контроля версий, которые дадут о них полное представление](https://tproger.ru/books/4-books-about-vcs/)


#### Git

- book: [Pro Git](https://git-scm.com/book/en)


### Deployment

#### Continuous Integration

#### Continuous Delivery

- book: [Continuous delivery. Практика непрерывных апдейтов](https://www.piter.com/product_by_id/87629352)


### Estimations

#### Planning Poker

### Debugging

#### Troubleshooting

#### Logging

- article: [Введение в ELK: собираем, фильтруем и анализируем большие данные](https://mkdev.me/posts/vvedenie-v-elk-sobiraem-filtruem-i-analiziruem-bolshie-dannye)


#### Monitoring

### Orchestration

#### Ansible

#### Puppet

#### Kubernetes

- book: [Kubernetes in Action](https://www.manning.com/books/kubernetes-in-action)


### Management

- book: [Goal: A Process of Ongoing Improvement](https://www.amazon.com/Goal-Process-Ongoing-Improvement/dp/0884271951)


#### Methodologies and Frameworks

- article: [Ещё раз про семь основных методологий разработки](https://habr.com/ru/company/edison/blog/269789/)


##### SCRUM

##### Kanban

##### Extreme Programming

##### The Twelve-Factor App

- article: [The Twelve-Factor App](https://12factor.net)


#### Paradigms and Models

##### Agile

- article: [Manifesto for Agile Software Development](https://agilemanifesto.org)


##### Waterfall

#### Time Management

- book: [Джедайские техники](https://www.mann-ivanov-ferber.ru/books/dzhedajskie-texniki/)


##### Pareto analysis

##### Getting Things Done

##### Pomodoro

## DevOps Practices

### Automation and Scripting

#### Shell scripting

#### Python scripting

#### Idempotency and error handling

### Containers

- article: [Get started with Docker](https://docs.docker.com/get-started/)


#### Images and registries

#### Docker

#### Container networking and storage

### Infrastructure as Code

- course: [Terraform tutorials](https://developer.hashicorp.com/terraform/tutorials)


#### Terraform

#### State and drift management

#### Reusable modules and infrastructure testing

### Delivery Pipelines

- book: [Google Site Reliability Engineering books](https://sre.google/books/)


#### Build, test, and artifact promotion

#### Rolling, blue-green, and canary deployments

#### Rollback and GitOps

### Cloud Infrastructure

- course: [Terraform tutorials](https://developer.hashicorp.com/terraform/tutorials)


#### Compute, storage, and virtual networks

#### Load balancing and autoscaling

#### Availability zones and cost management

### Observability

- article: [OpenTelemetry documentation](https://opentelemetry.io/docs/)


#### Metrics, logs, and traces

#### Dashboards and actionable alerts

#### OpenTelemetry

### Site Reliability Engineering

- book: [Google Site Reliability Engineering books](https://sre.google/books/)


#### SLIs, SLOs, and error budgets

#### Incident response and postmortems

#### Backups and disaster recovery

#### Capacity planning and toil reduction

### Platform Security

- book: [Google Site Reliability Engineering books](https://sre.google/books/)


#### Least privilege and identity management

#### Secrets and certificate management

#### Dependency and image scanning

#### Software supply chain security

