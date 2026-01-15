# Monitoring Setup Guide

This directory contains Kubernetes manifests for deploying Prometheus and Grafana monitoring to your Minikube cluster.

## 📊 Components

### Prometheus
- **Purpose**: Metrics collection and time-series database
- **Access**: http://localhost:30090 (NodePort)
- **Features**:
  - Scrapes Kubernetes cluster metrics
  - Monitors Flask webapp
  - Custom alerting rules
  - Service discovery

### Grafana
- **Purpose**: Visualization and dashboards
- **Access**: http://localhost:30030 (NodePort)
- **Credentials**: 
  - Username: `admin`
  - Password: `admin123` (change after first login!)
- **Features**:
  - Pre-configured Prometheus datasource
  - Kubernetes cluster dashboard
  - Real-time metrics visualization

## 🚀 Quick Start

### 1. Deploy Prometheus
```powershell
kubectl apply -f k8s/prometheus-deployment.yaml
```

### 2. Deploy Grafana
```powershell
kubectl apply -f k8s/grafana-deployment.yaml
```

### 3. Verify Deployments
```powershell
# Check if pods are running
kubectl get pods -n monitoring

# Check services
kubectl get svc -n monitoring
```

### 4. Access Dashboards

**Prometheus UI:**
```powershell
minikube service prometheus -n monitoring
# Or directly: http://localhost:30090
```

**Grafana UI:**
```powershell
minikube service grafana -n monitoring
# Or directly: http://localhost:30030
```

## 📈 Using Grafana

1. **Login** to Grafana (admin/admin123)
2. **Navigate** to Dashboards → Browse
3. **Select** "AI-DevOps Kubernetes Cluster" dashboard
4. **View** real-time metrics:
   - CPU usage
   - Memory usage
   - Pod counts
   - Node status

## 🔍 Prometheus Queries

Example queries to try in Prometheus:

```promql
# Total pods running
count(kube_pod_info)

# CPU usage by pod
sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)

# Memory usage
sum(container_memory_usage_bytes) by (pod)

# Flask app requests (if metrics endpoint added)
rate(flask_http_requests_total[5m])
```

## 🎯 Next Steps

### Add Metrics to Flask App
Update `webapp1/app.py` to expose Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, generate_latest
from flask import Response

# Define metrics
REQUEST_COUNT = Counter('flask_http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('flask_http_request_duration_seconds', 'HTTP request latency')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

@app.before_request
def before_request():
    REQUEST_COUNT.inc()
```

Then add `prometheus-client` to `webapp1/requirements.txt`.

### Create Custom Dashboards
1. In Grafana, click **"+"** → **Dashboard**
2. Add panels with custom queries
3. Save dashboard

### Set Up Alerts
Edit `prometheus-config` ConfigMap to add alerting rules:

```yaml
rule_files:
  - /etc/prometheus/alerts.yml

groups:
  - name: example
    rules:
    - alert: HighMemoryUsage
      expr: container_memory_usage_bytes > 1000000000
      for: 5m
      annotations:
        summary: "High memory usage detected"
```

## 🧹 Cleanup

To remove monitoring stack:
```powershell
kubectl delete -f k8s/grafana-deployment.yaml
kubectl delete -f k8s/prometheus-deployment.yaml
kubectl delete namespace monitoring
```

## 🔧 Troubleshooting

**Pods not starting?**
```powershell
kubectl describe pod <pod-name> -n monitoring
kubectl logs <pod-name> -n monitoring
```

**Can't access UI?**
```powershell
# Get service URL
minikube service list

# Port forward as alternative
kubectl port-forward -n monitoring svc/prometheus 9090:9090
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

**No metrics showing?**
- Check if Prometheus can scrape targets: http://localhost:30090/targets
- Verify service discovery is working
- Ensure RBAC permissions are correct

## 📚 Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
