from flask import Flask, jsonify, Response, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import time
import psutil

app = Flask(__name__)

# Prometheus metrics registry
registry = CollectorRegistry()

# Define custom metrics
REQUEST_COUNT = Counter(
    'flask_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

REQUEST_LATENCY = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    registry=registry
)

ACTIVE_REQUESTS = Gauge(
    'flask_active_requests',
    'Number of active requests',
    registry=registry
)

CPU_USAGE = Gauge(
    'flask_cpu_usage_percent',
    'CPU usage percentage',
    registry=registry
)

MEMORY_USAGE = Gauge(
    'flask_memory_usage_bytes',
    'Memory usage in bytes',
    registry=registry
)

@app.route('/')
def home():
    start_time = time.time()
    result = "Welcome to AI-Driven DevOps Pipeline! 🚀"
    
    # Track request
    REQUEST_COUNT.labels(method='GET', endpoint='home', status='200').inc()
    REQUEST_LATENCY.labels(method='GET', endpoint='home').observe(time.time() - start_time)
    ACTIVE_REQUESTS.inc()
    
    return result

@app.route('/status')
def status():
    start_time = time.time()
    
    # Update system metrics
    CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)
    
    result = jsonify({
        "status": "running",
        "uptime": "100%",
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_mb": round(psutil.Process().memory_info().rss / 1024 / 1024, 2)
    })
    
    # Track request
    REQUEST_COUNT.labels(method='GET', endpoint='status', status='200').inc()
    REQUEST_LATENCY.labels(method='GET', endpoint='status').observe(time.time() - start_time)
    
    return result

@app.route('/health')
def health():
    """Kubernetes liveness probe"""
    return jsonify({"status": "healthy"}), 200

@app.route('/ready')
def ready():
    """Kubernetes readiness probe"""
    return jsonify({"status": "ready"}), 200

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    # Update system metrics before serving
    CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)
    
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
