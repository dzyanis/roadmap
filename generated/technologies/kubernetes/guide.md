# Kubernetes

- article: [Kubernetes local learning environment](https://kubernetes.io/docs/setup/learning-environment/)


## Start here: prerequisites

- article: [Kubernetes local learning environment](https://kubernetes.io/docs/setup/learning-environment/)


### Process Creation, Execution, and Exit

- article: [OSTEP: processes](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-intro.pdf)


### Process and CPU Inspection (ps, top)

- article: [Linux process inspection with ps](https://man7.org/linux/man-pages/man1/ps.1.html)


### Bash

- article: [Bash manual](https://www.gnu.org/software/bash/manual/bash.html)


### DNS

- article: [Kubernetes networking model](https://kubernetes.io/docs/concepts/services-networking/)


### IP

- article: [Kubernetes networking model](https://kubernetes.io/docs/concepts/services-networking/)


### TCP

- article: [Kubernetes networking model](https://kubernetes.io/docs/concepts/services-networking/)


### Images and registries

- article: [Docker container concepts](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- article: [Docker images](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)


### YAML: mappings, sequences and indentation

- article: [YAML specification](https://yaml.org/spec/1.2.2/)


## Kubernetes

- article: [Learn Kubernetes basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)


### 1. Cluster architecture and API model

- article: [Kubernetes: 1. Cluster architecture and API model](https://kubernetes.io/docs/concepts/overview/components/)


#### Control plane, worker nodes and kubelet

- article: [Kubernetes: 1. Cluster architecture and API model](https://kubernetes.io/docs/concepts/overview/components/)


#### API objects, desired state and manifests

- article: [Kubernetes: 1. Cluster architecture and API model](https://kubernetes.io/docs/concepts/overview/components/)
- article: [Kubernetes objects and declarative management](https://kubernetes.io/docs/concepts/overview/working-with-objects/)


#### Controllers and reconciliation

- article: [Kubernetes: 1. Cluster architecture and API model](https://kubernetes.io/docs/concepts/overview/components/)
- article: [Kubernetes objects and declarative management](https://kubernetes.io/docs/concepts/overview/working-with-objects/)


### 2. Everyday tools and organization

- article: [Kubernetes: 2. Everyday tools and organization](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- article: [kubectl quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)


#### kubectl, contexts and namespaces

- article: [Kubernetes: 2. Everyday tools and organization](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- article: [kubectl quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)


#### Labels, selectors and annotations

- article: [Kubernetes: 2. Everyday tools and organization](https://kubernetes.io/docs/concepts/overview/working-with-objects/)


#### YAML manifests and API versions

- article: [Kubernetes: 2. Everyday tools and organization](https://kubernetes.io/docs/concepts/overview/working-with-objects/)


### 3. Application workloads

- article: [Kubernetes: 3. Application workloads](https://kubernetes.io/docs/concepts/workloads/controllers/)


#### Pods and container lifecycle

- article: [Kubernetes: 3. Application workloads](https://kubernetes.io/docs/concepts/workloads/controllers/)
- article: [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)


#### Deployments, ReplicaSets and rolling updates

- article: [Kubernetes: 3. Application workloads](https://kubernetes.io/docs/concepts/workloads/controllers/)
- article: [Deployments: rollout and rollback](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)


#### StatefulSets and stable identity

- article: [Kubernetes: 3. Application workloads](https://kubernetes.io/docs/concepts/workloads/controllers/)


#### DaemonSets and node services

- article: [Kubernetes: 3. Application workloads](https://kubernetes.io/docs/concepts/workloads/controllers/)


#### Jobs and CronJobs

- article: [Kubernetes: 3. Application workloads](https://kubernetes.io/docs/concepts/workloads/controllers/)


#### Rollout history and rollback

- article: [Kubernetes: 3. Application workloads](https://kubernetes.io/docs/concepts/workloads/controllers/)
- article: [Deployments: rollout and rollback](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)


### 4. Application configuration

- article: [Kubernetes: 4. Application configuration](https://kubernetes.io/docs/concepts/configuration/)


#### ConfigMaps and environment variables

- article: [Kubernetes: 4. Application configuration](https://kubernetes.io/docs/concepts/configuration/)
- article: [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)


#### Secrets and safe credential handling

- article: [Kubernetes: 4. Application configuration](https://kubernetes.io/docs/concepts/configuration/)
- article: [Secrets: access, encryption and security](https://kubernetes.io/docs/concepts/configuration/secret/)


#### Volumes and configuration mounts

- article: [Kubernetes: 4. Application configuration](https://kubernetes.io/docs/concepts/configuration/)
- article: [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)


### 5. Networking and traffic

- article: [Kubernetes: 5. Networking and traffic](https://kubernetes.io/docs/concepts/services-networking/)


#### Services, selectors and EndpointSlices

- article: [Kubernetes: 5. Networking and traffic](https://kubernetes.io/docs/concepts/services-networking/)
- article: [Kubernetes networking: services](https://kubernetes.io/docs/concepts/services-networking/service/)


#### Service discovery and cluster DNS

- article: [Kubernetes: 5. Networking and traffic](https://kubernetes.io/docs/concepts/services-networking/)
- article: [Kubernetes networking: dns](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)


#### Gateway API: GatewayClass, Gateway and HTTPRoute

- article: [Kubernetes: 5. Networking and traffic](https://kubernetes.io/docs/concepts/services-networking/)
- article: [Kubernetes networking: gateway](https://kubernetes.io/docs/concepts/services-networking/gateway/)


#### Ingress API (frozen) and controller requirements

- article: [Kubernetes: 5. Networking and traffic](https://kubernetes.io/docs/concepts/services-networking/)
- article: [Kubernetes networking: ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)


#### NetworkPolicies and supporting network plugins

- article: [Kubernetes: 5. Networking and traffic](https://kubernetes.io/docs/concepts/services-networking/)
- article: [Kubernetes networking: policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)


### 6. Persistent storage

- article: [Kubernetes: 6. Persistent storage](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)


#### PersistentVolumes and PersistentVolumeClaims

- article: [Kubernetes: 6. Persistent storage](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)


#### StorageClasses and dynamic provisioning

- article: [Kubernetes: 6. Persistent storage](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- article: [StorageClasses](https://kubernetes.io/docs/concepts/storage/storage-classes/)


#### Access modes, reclaim policy and data lifecycle

- article: [Kubernetes: 6. Persistent storage](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)


### 7. Scheduling and reliability

- article: [Kubernetes: 7. Scheduling and reliability](https://kubernetes.io/docs/concepts/scheduling-eviction/)


#### CPU/memory requests and limits

- article: [Kubernetes: 7. Scheduling and reliability](https://kubernetes.io/docs/concepts/scheduling-eviction/)
- article: [Kubernetes reliability: resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)


#### Startup, readiness and liveness probes

- article: [Kubernetes: 7. Scheduling and reliability](https://kubernetes.io/docs/concepts/scheduling-eviction/)
- article: [Kubernetes reliability: probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)


#### Node affinity, taints and tolerations

- article: [Kubernetes: 7. Scheduling and reliability](https://kubernetes.io/docs/concepts/scheduling-eviction/)


#### PodDisruptionBudgets and voluntary disruption

- article: [Kubernetes: 7. Scheduling and reliability](https://kubernetes.io/docs/concepts/scheduling-eviction/)
- article: [Kubernetes reliability: disruptions](https://kubernetes.io/docs/tasks/run-application/configure-pdb/)


#### Horizontal autoscaling and metrics dependencies

- article: [Kubernetes: 7. Scheduling and reliability](https://kubernetes.io/docs/concepts/scheduling-eviction/)
- article: [Kubernetes reliability: scaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)


### 8. Workload security

- article: [Kubernetes: 8. Workload security](https://kubernetes.io/docs/concepts/security/)


#### ServiceAccounts and workload identity

- article: [Kubernetes: 8. Workload security](https://kubernetes.io/docs/concepts/security/)


#### RBAC and least privilege

- article: [Kubernetes: 8. Workload security](https://kubernetes.io/docs/concepts/security/)
- article: [RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)


#### Security contexts and Pod Security Admission

- article: [Kubernetes: 8. Workload security](https://kubernetes.io/docs/concepts/security/)
- article: [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)


### 9. Troubleshooting applications

- article: [Kubernetes: 9. Troubleshooting applications](https://kubernetes.io/docs/tasks/debug/debug-application/)


#### Logs, events, describe and metrics

- article: [Kubernetes: 9. Troubleshooting applications](https://kubernetes.io/docs/tasks/debug/debug-application/)


#### Pending, ImagePullBackOff and CrashLoopBackOff

- article: [Kubernetes: 9. Troubleshooting applications](https://kubernetes.io/docs/tasks/debug/debug-application/)


#### Debug Service selectors, endpoints and DNS

- article: [Kubernetes: 9. Troubleshooting applications](https://kubernetes.io/docs/tasks/debug/debug-application/)


#### Debug Pending PVCs and volume mounts

- article: [Kubernetes: 9. Troubleshooting applications](https://kubernetes.io/docs/tasks/debug/debug-application/)


### 10. Packaging and delivery

- article: [Kubernetes: 10. Packaging and delivery](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)


#### Helm charts and release lifecycle

- article: [Kubernetes: 10. Packaging and delivery](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- article: [Helm: quick start](https://helm.sh/docs/intro/quickstart/)


#### Kustomize bases and overlays

- article: [Kubernetes: 10. Packaging and delivery](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)


#### GitOps reconciliation and drift

- article: [Kubernetes: 10. Packaging and delivery](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- article: [Flux: GitOps getting started](https://fluxcd.io/flux/get-started/)


### Further study: cluster administration

- article: [Kubernetes: Further study: cluster administration](https://kubernetes.io/docs/setup/production-environment/)


#### Managed clusters, kubeadm and topology choices

- article: [Kubernetes: Further study: cluster administration](https://kubernetes.io/docs/setup/production-environment/)


#### Version skew, upgrades and node maintenance

- article: [Kubernetes: Further study: cluster administration](https://kubernetes.io/docs/setup/production-environment/)
- article: [Kubernetes administration: upgrades](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)


#### etcd snapshots and recovery drills

- article: [Kubernetes: Further study: cluster administration](https://kubernetes.io/docs/setup/production-environment/)
- article: [Kubernetes administration: recovery](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)


#### CRDs, operators and admission webhooks

- article: [Kubernetes: Further study: cluster administration](https://kubernetes.io/docs/setup/production-environment/)
- article: [Kubernetes administration: extensions](https://kubernetes.io/docs/concepts/extend-kubernetes/)


## Practice: local application milestones

- article: [Kubernetes local learning environment](https://kubernetes.io/docs/setup/learning-environment/)


### 1. Create a local cluster and inspect nodes

- article: [1. Create a local cluster and inspect nodes](https://kind.sigs.k8s.io/docs/user/quick-start/)


### 2. Deploy an application and inspect reconciliation

- article: [2. Deploy an application and inspect reconciliation](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/)


### 3. Expose a Service and test port-forwarding

- article: [3. Expose a Service and test port-forwarding](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)


### 4. Inject ConfigMap and Secret values

- article: [4. Inject ConfigMap and Secret values](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)


### 5. Mount a PVC and verify data after Pod replacement

- article: [5. Mount a PVC and verify data after Pod replacement](https://kubernetes.io/docs/tutorials/configuration/configure-persistent-volume-storage/)


### 6. Update an image and roll back a failed rollout

- article: [6. Update an image and roll back a failed rollout](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)


### 7. Break a selector or image tag, diagnose and repair

- article: [7. Break a selector or image tag, diagnose and repair](https://kubernetes.io/docs/tasks/debug/debug-application/)


