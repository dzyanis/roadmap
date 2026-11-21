# AWS Solutions Architect learning path

A subject describes a body of knowledge; a role roadmap composes subjects into
a learning path. Start with the shared prerequisites, study the vendor-neutral
architecture subject, then use the AWS subject to map requirements to platform
choices. Finish with the three reviews below. Build with
`make aws-solutions-architect`; `make site` discovers the roadmap automatically.
The [generated guide](../../../generated/roles/aws-solutions-architect/guide.md)
contains readings for each branch and exercise.

AWS Well-Architected provides the review framework: operational excellence,
security, reliability, performance efficiency, cost optimization and
sustainability. Use the current official documentation for the selected Region,
service features and quotas. Certification is an optional check of coverage;
this initial roadmap is not an exhaustive exam syllabus.

## Design exercises

Each exercise can be completed on paper without creating AWS resources. Submit
requirements and assumptions, a context/deployment diagram with trust boundaries,
two alternatives, an ADR explaining the choice, failure scenarios, an operating
plan and a cost estimate. Explain the tradeoffs rather than treating a service
name as a solution. Record Region, traffic assumptions, data size, retention,
service quotas and pricing date in the estimate.

| Exercise | Design task | Review evidence |
| --- | --- | --- |
| Resilient web application | Design a small authenticated application with static assets, an API and relational data. Compare EC2/Auto Scaling with ECS/Fargate and Lambda where the workload fits. Discuss CloudFront/S3, load balancing, private database access and multi-AZ deployment. | Define availability and latency targets; trace a request and its permissions; explain a zone failure, database failover, cache staleness and deployment rollback. Distinguish a read replica from HA failover. Include monitoring, backups and restore tests. |
| Event-driven workload | Design asynchronous document processing. Compare SQS work queues, SNS fan-out and EventBridge routing; decide whether Step Functions coordination is needed. | Trace a duplicated, delayed and permanently failing event. Show idempotency keys, retry bounds, dead-letter handling, ordering assumptions, consumer capacity and least-privilege access. Explain why the application must still handle duplicate effects even when a service offers deduplication. |
| Recovery and cost review | Give the application explicit recovery time and recovery point objectives. Compare backup/restore, pilot light and warm standby; justify whether a second Region is needed. | Produce a recovery runbook, timed restore-test plan and estimated data-loss window. Compare normal-operation and recovery costs, replication lag, retained snapshots and data transfer. Explain how backups address corruption that replication can propagate. |

Use the [AWS Pricing Calculator](https://calculator.aws/) and the applicable
service pricing pages. Separate steady-state, peak, recovery and retained-data
costs. Include operator effort when comparing managed and self-managed systems.
Budget alerts are notifications, not a guarantee that spending will stop.

## Optional sandbox practice

Before deploying anything, use a dedicated sandbox account/environment, temporary
credentials, an explicit Region and resource tags. Estimate costs, set billing
alerts, and choose a small, bounded version of one exercise. Follow the linked
official tutorials for current deployment steps; no deployment is required by
this repository build. Do not assume Free Tier eligibility or zero cost.

For the web design, a short-lived load balancer, compute task/instance and small
database can demonstrate request routing and access boundaries. The full HA
design can remain a reviewed diagram. For the event design, use synthetic files
and a bounded event count; verify success, retries and a dead-letter case. For
recovery, create disposable sample data, make a backup, restore to a temporary
resource, and record elapsed recovery time and observed data loss.

| Potential charges | Teardown and verification |
| --- | --- |
| EC2/ECS/Fargate compute, load balancers, NAT gateways and public IPv4 addresses | Scale down and remove application resources and load balancers; delete dedicated gateways and release allocated addresses. Check every Region used. |
| RDS/Aurora instances, EBS/EFS storage and snapshots | Delete disposable databases and volumes; inspect final/retained snapshots and retained backups separately. Remove only lab copies after the restore exercise. |
| S3 versions, replication and requests; DynamoDB and caches | Empty lab buckets including versions/delete markers as required; disable lab replication and remove replicas, tables and cache resources. Check retention or object-lock settings before the exercise. |
| Lambda, SQS/SNS/EventBridge and Step Functions requests | Disable producers, schedules and event sources first; remove consumers, workflows, rules, queues and topics so retries cannot keep generating work. |
| CloudWatch logs/metrics, backup vault recovery points, secrets and keys | Apply short log retention; remove lab logs and recovery points, and schedule deletion of lab secrets/keys where required. Note delayed deletion and retained resources. |
| Cross-AZ/cross-Region transfer, DNS and edge delivery | Include transfer in estimates; remove dedicated DNS records/hosted zones and disable/delete lab distributions when no longer needed. |

Delete the infrastructure stack if one was used, then inspect resources with
retention policies and resources created outside the stack. Review the account's
resource inventory and billing after usage data arrives. Stopping an instance or
deleting a stack does not prove that all storage, snapshots and networking
charges have ended. Never tear down shared organizational infrastructure.

## Reuse and scope

`subjects/architecture` has no AWS dependency. It reuses existing distributed-data,
SLO and backup topics through fragments; its concepts remain vendor-neutral even
when a reading uses a particular platform as an example. `subjects/aws` contains
AWS choices and reuses the existing SQS topic ID rather than defining it again.
Neither subject requires the role root or the other subject.

The role imports selected networking, OS and container-image prerequisites from
existing fragments. Original topic IDs, labels, edges and resource associations
remain available in their original subjects. Existing role roadmaps do not
implicitly acquire the new architecture or AWS branches.

ECS/EKS/Fargate coverage concerns AWS orchestration and compute choices. For Pods,
controllers, Services and cluster fundamentals, use the separate
[Kubernetes roadmap](../../technologies/kubernetes/README.md). EKS is a choice,
not a mandatory prerequisite for every AWS architecture.

The first path prioritizes common workloads and architectural judgment. Deep
multi-Region/hybrid design is further study. Exhaustive service catalogs,
provider-specific production runbooks and full certification mapping remain
outside scope. Numbered branches suggest a learning order; containment edges are
not typed prerequisites. The conventional `backend` root ID is displayed as
AWS Solutions Architect. All outputs derive from XML; the role build also emits
JSON for the website.
