# Kubernetes learning path

Start with the prerequisites, work through the numbered application branches,
then use the milestones below to combine them. Cluster administration is further
study. The [generated guide](../../../generated/technologies/kubernetes/guide.md)
links official readings for every major branch and each milestone. Build with
`make kubernetes`; `make site` automatically includes this technology roadmap.

Use a disposable local kind cluster with a supported container runtime and
kubectl. Follow the [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
for installation and select a supported node image. Record the kind, Kubernetes
and kubectl versions in your notes; check documentation for your server version.
Before each exercise, verify `kubectl config current-context` is your local
cluster. Create a `roadmap-lab` namespace and use it for application resources.

| Milestone | Exercise | Evidence of completion |
| --- | --- | --- |
| 1. Local cluster | Create `kind create cluster --name roadmap-lab`; inspect nodes, namespaces and system Pods. | Nodes become Ready; explain the control plane and worker responsibilities. |
| 2. Deployment | Apply a small web Deployment with a deliberately chosen image tag; inspect its Deployment, ReplicaSet and Pods. Delete one Pod. | The controller recreates it; explain desired versus observed state. |
| 3. Service | Add a ClusterIP Service with matching selectors. Use `kubectl -n roadmap-lab port-forward service/web 8080:80` with ports matching your application. | A local request reaches the app; explain selectors, EndpointSlices and service DNS. Port-forwarding is a lab access method, not public ingress. |
| 4. Configuration | Mount a ConfigMap and a Secret containing dummy values, then change configuration. | Show the value inside the Pod and explain when a restart is needed for environment variables versus mounted files. Keep credentials out of Git; base64 encoding is not encryption. |
| 5. Persistence | Inspect available StorageClasses; create a PVC and mount it in a Pod. Write a marker, replace the Pod while retaining the PVC, then read it again. | The marker survives Pod replacement. Explain why local-cluster storage is not resilient to deleting the cluster, and inspect the reclaim policy. If dynamic provisioning is absent, follow the linked local PV tutorial. |
| 6. Update and rollback | Set readiness probes, update the Deployment image to a second valid tag, inspect rollout status/history, then roll back. | Requests recover and the expected image is restored. Explain how readiness affects traffic and how a failed rollout differs from a successful update. |
| 7. Troubleshooting | Introduce an invalid image tag and a mismatched Service selector in separate experiments. Inspect events, describe output, logs when available and EndpointSlices; repair each fault. | Write a symptom → evidence → cause → fix note for both. Distinguish an image pull failure from a running but unreachable app. |

Afterward, stop port-forwarding, delete the namespace, then run
`kind delete cluster --name roadmap-lab`. Local container images may remain in
the container runtime cache. These exercises need no cloud LoadBalancer or
managed cluster. Do not apply them to a shared or production context.

Networking includes Services/DNS first, then Gateway API and Ingress. Current
[Kubernetes guidance](https://kubernetes.io/docs/concepts/services-networking/ingress/)
recommends Gateway API for new capabilities; Ingress is frozen, not removed.
Both require a compatible implementation/controller. NetworkPolicy enforcement
also depends on the network plugin. The basic milestones use port-forwarding,
so they do not assume kind includes a Gateway controller or policy enforcement.

Continue with requests/limits, probes, placement and disruption budgets; then
ServiceAccounts, RBAC and Pod Security Admission. Helm, Kustomize and GitOps
introduce delivery choices. Autoscaling needs the relevant metrics pipeline.
Managed clusters/kubeadm, upgrades, etcd recovery and extensions are advanced
study; a local workload lab does not demonstrate production administration skill.

## Composition and compatibility

`subjects/kubernetes` is reusable. It uses the existing `dev_orchestration_k8s`
topic from a small software-development fragment. The existing role roadmaps
still include that same topic and its Kubernetes in Action book; they do not
implicitly expand into the new detailed curriculum.

Prerequisites reuse seven existing topic IDs from small fragments in operating
systems, networking and DevOps. The original subjects include those fragments,
so each topic has one definition. The Kubernetes roadmap adds only the selected
nodes, their learning resources and a YAML prerequisite; it does not import
entire unrelated subject trees. Existing subject labels, edges and resource
associations are preserved. The roadmap root keeps the conventional `backend`
ID required by the existing build, displayed as Kubernetes.

Numbering conveys the suggested learning order. Current `contains` edges are
outline relationships, not typed prerequisites. The practical curriculum focuses
on application operation; exhaustive administration, provider-specific setup and
certification mapping remain outside this initial scope. Resources were checked
against official project documentation during #41 implementation. The milestone
instructions are learning exercises, not an automatically executed cluster test.
