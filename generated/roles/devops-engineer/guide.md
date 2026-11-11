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

### SQL

- book: [SQL Bible](https://www.amazon.com/SQL-Bible-Alex-Kriegel/dp/0470229063)


### Indexes

### Transactions

### Principles

### Relational

#### Multiversion Concurrency Control

##### Firebird

##### PostgreSQL

##### Oracle

- book: [Oracle PL/SQL Programming: Covers Versions Through Oracle Database 12c](https://www.amazon.com/Oracle-PL-SQL-Programming-Versions/dp/1449324452)


##### MySQL

#### Blocking

##### MySQL

#### ACID

#### Object-oriented

### NOSQL

- article: [NOSQL](https://martinfowler.com/nosql.html)
- book: [NoSQL Distilled](https://martinfowler.com/books/nosql.html)


#### CAP Theorem

#### BASE

#### Graph database

##### OrientDB

##### Neo4j

#### Document base

##### MongoDB

#### Column base

##### Redis

##### ClickHouse

#### Wide column base

#### Time series

### Search Engines

#### Elasticseaerch

#### Sphinx

### Message Broker

#### Kafka

#### RabbitMQ

#### Amazon Simple Queue Service

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

