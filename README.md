# 🚀 MLOps Week 7: Stress Testing, Observability & Scaling the IRIS API


## 📌 Executive Summary

This repository contains the complete implementation of **Week 7: Stress Testing, Observability & Scaling an ML Model in Production**. 

Building upon the GKE continuous deployment baseline from Week 6, this project evaluates the resiliency, scaling behavior, and resource bottlenecks of a containerized **IRIS Flower Classification FastAPI** service under high-concurrency synthetic workloads.

### Key Milestones Delivered:
1. **Containerized Deployment on GKE:** Deployed FastAPI model serving endpoint (`/predict/`) backed by Docker & Artifact Registry.
2. **Automated CI/CD Load Testing:** Extended GitHub Actions (`.github/workflows/cd.yml`) with automated `wrk` benchmarking scripts (`post.lua`) upon every push.
3. **High-Concurrency Benchmarking:** Conducted stress tests simulating up to **2,000 concurrent connections** to evaluate throughput (Req/sec), latency distribution, and error profiles.
4. **Horizontal Pod Autoscaling (HPA):** Implemented target CPU utilization scaling (`50%` CPU target, `minReplicas: 1`, `maxReplicas: 3`). Verified dynamic scaling during CPU spikes up to **497%**.
5. **Full-Stack Observability:** Configured real-time log ingestion via **GCP Cloud Logging** and infrastructure telemetry via **GCP Cloud Monitoring**.
6. **Constrained Scaling Analysis:** Analyzed performance degradation under locked single-pod capacity (`maxReplicas: 1`) to isolate compute bottlenecks.

---

## 🏗 System Architecture

```text
                                  +-------------------------------------------------------+
                                  |                 GCP Cloud Infrastructure              |
                                  |                                                       |
  +------------------+            |  +--------------------+     +----------------------+  |
  |   wrk / Client   | POST /predict|  |  GKE LoadBalancer  |     |   Cloud Monitoring   |  |
  |  Stress Tester   |----------->|  |    (Port 80)       |     |  & Cloud Logging     |  |
  +------------------+            |  +---------+----------+     +----------+-----------+  |
                                  |            |                           ^              |
                                  |            v                           | Telemetry    |
                                  |  +-------------------------------------+-----------+  |
                                  |  |              iris-api Deployment                |  |
                                  |  |                                                 |  |
                                  |  |  +----------------+  +----------------+         |  |
                                  |  |  | Pod 1 (Target) |  | Pod 2 (HPA)    | ...     |  |
                                  |  |  | containerPort  |  | containerPort  |         |  |
                                  |  |  |     :8000      |  |     :8000      |         |  |
                                  |  |  +----------------+  +----------------+         |  |
                                  |  +-------------------------------------------------+  |
                                  |                            ^                          |
                                  |                            | Scale (1 -> 3 Pods)      |
                                  |                 +----------+----------+               |
                                  |                 |   Horizontal Pod    |               |
                                  |                 |  Autoscaler (HPA)   |               |
                                  |                 +---------------------+               |
                                  +-------------------------------------------------------+
```
```text
📂 Repository StructurePlaintext23F1001473_MLOPS_WEEKLY_ASSIGNMENT/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # MLOps Continuous Integration (Linting, Tests, DVC)
│       └── cd.yml                 # MLOps CD Pipeline with Automated wrk Stress Test
├── api/
│   ├── Dockerfile                 # Container specification exposing port 8000
│   ├── main.py                    # FastAPI application serving /predict/ endpoint
│   ├── model.joblib               # Serialized DecisionTreeClassifier model
│   └── requirements.txt           # Production Python dependencies
├── k8s/
│   ├── deployment.yaml            # Kubernetes Deployment with Recreate strategy & resource specs
│   ├── service.yaml               # Kubernetes LoadBalancer Service (Port 80 -> 8000)
│   └── hpa.yaml                   # HorizontalPodAutoscaler (CPU 50%, min: 1, max: 3)
├── post.lua                       # wrk Lua script formatting JSON POST payloads
└── README.md                      # Project documentation & benchmark analysis
```

📊 Benchmark & Performance ComparisonAll stress tests were conducted using wrk against the live External LoadBalancer IP.Test ScenarioConcurrency (-c)Target CPUActive ReplicasRequests / SecAvg LatencySocket TimeoutsHPA StatusBaseline CI/CD Test50 conn / 15sN/A1123.62397.56 ms0DisabledTask 2: High Concurrency1,000 conn / 30sN/A1114.661.39 s2,408DisabledTask 3: HPA Autoscaling1,000 conn / 45s50% Target1 ➔ 3109.091.44 s3,661SuccessfulRescale (497%/50%)Task 5: Constrained Scaling2,000 conn / 30s50% Target1 (Capped)112.581.16 s2,653ScalingLimited (162%/50%)Key Observations:CPU Saturation: Under 1,000+ concurrent connections, a single pod's CPU utilization surges up to 497% of its request limit (100m), causing request queuing and latency spikes.HPA Scaling Dynamics: When enabled, the HPA controller successfully calculated CPU metrics (ScalingActive) and issued a SuccessfulRescale event to expand the cluster footprint from 1 to 3 pods.Constrained Scaling Bottlenecks: Restricting maxReplicas: 1 forced the system into a ScalingLimited state (TooManyReplicas), proving that single-instance compute acts as the primary bottleneck for throughput plateau (~114 Req/sec).🛠 Kubernetes Manifests Specification1. Deployment (k8s/deployment.yaml)Configured with strategy.type: Recreate to prevent resource deadlocks during rolling updates on single-node nodes:YAMLapiVersion: apps/v1
kind: Deployment
metadata:
  name: iris-api
spec:
  replicas: 1
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: iris-api
  template:
    metadata:
      labels:
        app: iris-api
    spec:
      containers:
      - name: iris-api
        image: us-central1-docker.pkg.dev/f1001473-mlops-week1/iris-repo/iris-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
2. Service (k8s/service.yaml)Exposes HTTP port 80 externally and routes traffic to container port 8000:YAMLapiVersion: v1
kind: Service
metadata:
  name: iris-service
spec:
  type: LoadBalancer
  selector:
    app: iris-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
3. Horizontal Pod Autoscaler (k8s/hpa.yaml)YAMLapiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: iris-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: iris-api
  minReplicas: 1
  maxReplicas: 3
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
    
⚡ Automated CI/CD Workflow (.github/workflows/cd.yml)The CD pipeline executes automatically on pushes to week_7:PlaintextCheckout ➔ GCP Auth ➔ Build Docker Image ➔ Push to GAR ➔ Get GKE Credentials ➔ Deploy K8s ➔ Install wrk ➔ Run Load Test
Automated Benchmark Execution in GitHub Actions:Bashwrk -t2 -c50 -d15s -s post.lua http://${EXTERNAL_IP}/predict/

🔍 GCP Observability & Monitoring1. GCP Cloud LoggingFiltered log query for container stdout/stderr:Plaintextresource.type="k8s_container"
resource.labels.cluster_name="iris-cluster"
resource.labels.namespace_name="default"
labels."k8s-pod/app"="iris-api"
Verified Log Output:PlaintextINFO:     10.12.0.1:5284 - "POST /predict/ HTTP/1.1" 200 OK
INFO:     10.12.0.1:51428 - "POST /predict/ HTTP/1.1" 200 OK
INFO:     10.12.0.1:57939 - "POST /predict/ HTTP/1.1" 200 OK
2. GCP Cloud MonitoringMonitored real-time telemetry metrics under GKE Workloads > iris-api > Observability:CPU Utilization (%)Memory RSS UtilizationNetwork Bytes In/Out💻 Quick Start & Reproducibility Guide1. Verify API ConnectionBashexport EXTERNAL_IP=$(kubectl get svc iris-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

curl -X POST http://${EXTERNAL_IP}/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
Output: {"predicted_class":"setosa"}2. Run High-Concurrency Load TestBashulimit -n 10000
wrk -t4 -c1000 -d30s -s post.lua http://${EXTERNAL_IP}/predict/
3. Check HPA StatusBashkubectl get hpa
kubectl get pods
