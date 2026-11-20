# AWS Solutions Architect

- article: [AWS Solutions Architect learning and optional certification](https://aws.amazon.com/certification/certified-solutions-architect-associate/)


## Start here: shared prerequisites

- article: [AWS networking foundations](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)


### DNS

- article: [AWS networking foundations](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)


### IP

- article: [AWS networking foundations](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)


### TCP

- article: [AWS networking foundations](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)


### Process Creation, Execution, and Exit

- article: [OSTEP: processes](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf)


### Process and CPU Inspection (ps, top)

- article: [Linux ps manual](https://man7.org/linux/man-pages/man1/ps.1.html)


### Bash

- article: [Bash manual](https://www.gnu.org/software/bash/manual/bash.html)


### Images and registries

- article: [Docker containers and images](https://docs.docker.com/learn/content/what-is-a-container/)


## Architecture foundations

- article: [arc42 architecture documentation guide](https://docs.arc42.org/home/)


### Requirements and quality attributes

- article: [arc42 quality requirements](https://docs.arc42.org/section-10/)


#### Stakeholders, constraints and workload assumptions

- article: [arc42 quality requirements](https://docs.arc42.org/section-10/)


#### Measurable quality scenarios and tradeoffs

- article: [arc42 quality requirements](https://docs.arc42.org/section-10/)


### Communicating architecture decisions

- article: [arc42 architecture decisions](https://docs.arc42.org/section-9/)


#### System context, boundaries and dependencies

- article: [arc42 architecture decisions](https://docs.arc42.org/section-9/)
- article: [C4 system context diagrams](https://c4model.com/diagrams/system-context)


#### ADRs: context, alternatives and consequences

- article: [arc42 architecture decisions](https://docs.arc42.org/section-9/)


### Availability and fault tolerance

- article: [Google SRE: addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)


#### Failure domains, redundancy and graceful degradation

- article: [Google SRE: addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)


#### Timeouts, bounded retries and idempotency

- article: [Google SRE: addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)


#### RTO, RPO and recovery testing

- article: [Google SRE: addressing cascading failures](https://sre.google/sre-book/addressing-cascading-failures/)
- article: [Google SRE: data integrity and recovery](https://sre.google/sre-book/data-integrity/)


#### SLIs, SLOs, and error budgets

- article: [Google SRE: service level objectives](https://sre.google/sre-book/service-level-objectives/)


#### Backups and disaster recovery

- article: [Google SRE: data integrity and recovery](https://sre.google/sre-book/data-integrity/)


### Scalability and data tradeoffs

- article: [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)


#### Capacity, bottlenecks and horizontal scaling

- article: [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)


#### Caching, invalidation and stale reads

- article: [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)
- article: [Cache-aside pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)


#### Replication and replication lag

- article: [Cassandra: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)


#### Partitioning and sharding

- article: [Cassandra: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)


#### Consistency and availability tradeoffs

- article: [Cassandra: partitioning, replication and consistency](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html)


### Asynchronous communication

- article: [Queue-based load leveling pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling)


#### Queues, backpressure and load leveling

- article: [Queue-based load leveling pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling)


#### Delivery semantics, deduplication and poison messages

- article: [Queue-based load leveling pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling)


### Security boundaries

- article: [OWASP threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)


#### Identity, least privilege and trust boundaries

- article: [OWASP threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)


#### Data classification, encryption and threat modeling

- article: [OWASP threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)


### Cost and operational ownership

- article: [Google SRE: eliminating toil](https://sre.google/sre-book/eliminating-toil/)
- article: [FinOps framework: business value and cost ownership](https://www.finops.org/framework/)


#### Total cost: capacity, traffic and people

- article: [Google SRE: eliminating toil](https://sre.google/sre-book/eliminating-toil/)
- article: [FinOps framework: business value and cost ownership](https://www.finops.org/framework/)


#### Managed versus self-managed components

- article: [Google SRE: eliminating toil](https://sre.google/sre-book/eliminating-toil/)


## AWS platform choices

- article: [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)


### 1. Cloud foundations

- article: [AWS overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)


#### Regions, Availability Zones and service scope

- article: [AWS overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- article: [AWS Regions and Availability Zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)


#### Accounts, Organizations and environment boundaries

- article: [AWS overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- article: [AWS Organizations concepts](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html)


#### Shared responsibility and managed-service boundaries

- article: [AWS overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- article: [AWS shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/)


### 2. Identity and data protection

- article: [AWS security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)


#### IAM roles, policies and least privilege

- article: [AWS security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- article: [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)


#### IAM Identity Center and temporary credentials

- article: [AWS security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- article: [IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)


#### KMS encryption and key permissions

- article: [AWS security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- article: [AWS KMS concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html)


#### Secrets Manager and rotation

- article: [AWS security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- article: [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)


#### CloudTrail audit events and accountability

- article: [AWS security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- article: [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)


### 3. Networking and delivery

- article: [Amazon VPC concepts](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)


#### VPC subnets, routes, security groups and NACLs

- article: [Amazon VPC concepts](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)


#### Internet/NAT gateways, endpoints and VPN choices

- article: [Amazon VPC concepts](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)


#### Route 53 DNS and health-based routing

- article: [Amazon VPC concepts](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- article: [Amazon Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)


#### Elastic Load Balancing and health checks

- article: [Amazon VPC concepts](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- article: [Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)


#### CloudFront edge caching and origin protection

- article: [Amazon VPC concepts](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- article: [Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)


### 4. Compute selection

- article: [AWS compute choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html)


#### EC2: virtual machines and operational control

- article: [AWS compute choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html)


#### ECS versus EKS; Fargate versus node management

- article: [AWS compute choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html)
- article: [Containers on AWS](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/containers.html)


#### Lambda: event-driven functions and execution limits

- article: [AWS compute choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html)
- article: [AWS Lambda overview and compute choices](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)


### 5. Storage selection

- article: [AWS storage choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/storage-services.html)


#### S3: object storage, versioning and lifecycle

- article: [AWS storage choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/storage-services.html)
- article: [S3 lifecycle management](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)


#### EBS: block storage tied to Availability Zones

- article: [AWS storage choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/storage-services.html)


#### EFS: shared file storage and access patterns

- article: [AWS storage choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/storage-services.html)


### 6. Data services and access patterns

- article: [AWS database choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html)


#### RDS and Aurora: relational transactions

- article: [AWS database choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html)


#### DynamoDB: keys, access patterns and capacity

- article: [AWS database choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html)


#### ElastiCache: latency and cache consistency

- article: [AWS database choices](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html)


### 7. Integration and workflows

- article: [AWS application integration](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/application-integration.html)


#### SNS: publish/subscribe fan-out

- article: [AWS application integration](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/application-integration.html)


#### EventBridge: event routing and integration

- article: [AWS application integration](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/application-integration.html)


#### Step Functions: workflow coordination

- article: [AWS application integration](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/application-integration.html)


#### Retries, idempotency and dead-letter handling

- article: [AWS application integration](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/application-integration.html)
- article: [SQS: queue semantics and reliable consumers](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)


#### Amazon Simple Queue Service

- article: [SQS: queue semantics and reliable consumers](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)


### 8. Reliability and operations

- article: [AWS reliability pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)


#### Multi-AZ design and failure isolation

- article: [AWS reliability pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- article: [AWS Regions and Availability Zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)


#### Auto Scaling, health signals and quotas

- article: [AWS reliability pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)


#### CloudWatch metrics, logs and alarms

- article: [AWS reliability pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- article: [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)


#### AWS Backup, snapshots and restore tests

- article: [AWS reliability pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- article: [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html)


### 9. Delivery, governance and cost

- article: [AWS operational excellence pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)


#### CloudFormation and CDK: repeatable environments

- article: [AWS operational excellence pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
- article: [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- article: [AWS CDK: infrastructure through CloudFormation](https://docs.aws.amazon.com/cdk/v2/guide/home.html)


#### Organizations SCPs and Config compliance checks

- article: [AWS operational excellence pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
- article: [Service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
- article: [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)


#### Budgets, Cost Explorer, tagging and lifecycle costs

- article: [AWS operational excellence pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
- article: [AWS cost optimization pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- article: [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)


### Further study: multi-Region and hybrid design

- article: [Disaster recovery options on AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)


#### Backup/restore, pilot light and warm standby

- article: [Disaster recovery options on AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)


#### Direct Connect and hybrid network tradeoffs

- article: [Disaster recovery options on AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)
- article: [AWS Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)


## Practice: architecture reviews

- article: [AWS Well-Architected review framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- article: [AWS Pricing Calculator](https://calculator.aws/)


### 1. Design a resilient web application

- article: [AWS Well-Architected review framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)


### 2. Design an event-driven workload

- article: [AWS Serverless Lens](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html)


### 3. Review recovery objectives and cost

- article: [AWS recovery strategies](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)
- article: [AWS Pricing Calculator](https://calculator.aws/)


