import psutil
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Function to collect system metrics
def collect_metrics():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }

# Function to analyze anomalies using Isolation Forest (ML model)
def detect_anomalies(metric_history):
    clf = IsolationForest(contamination=0.1)  # Detect anomalies in 10% of the data
    clf.fit(metric_history)
    predictions = clf.predict(metric_history)
    return predictions[-1] == -1  # Return True if latest metric is an anomaly

# Function to visualize system metrics
def visualize_metrics(cpu_usage, memory_usage):
    plt.figure(figsize=(10, 5))
    plt.plot(cpu_usage, label="CPU Usage (%)", color='r')
    plt.plot(memory_usage, label="Memory Usage (%)", color='b')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Usage (%)")
    plt.title("System Metrics Over Time")
    plt.legend()
    # plt.show()  # Commented out for automated pipeline execution
    plt.savefig('logs/system_metrics_plot.png')
    print("📊 System metrics plot saved to logs/system_metrics_plot.png")

if __name__ == "__main__":
    print("\n=== AI-Powered Monitoring Agent Running ===")
    cpu_history = []
    memory_history = []

    for _ in range(10):  # Monitor for 10 seconds (reduced from 30 for pipeline speed)
        metrics = collect_metrics()
        cpu_history.append(metrics["cpu"])
        memory_history.append(metrics["memory"])

        print(f"CPU: {metrics['cpu']}% | Memory: {metrics['memory']}% | Disk: {metrics['disk']}%")

        # Convert lists to NumPy array for anomaly detection
        if len(cpu_history) > 5:
            metric_data = np.array([cpu_history[-5:], memory_history[-5:]]).T  # Last 5 data points
            if detect_anomalies(metric_data):
                print("⚠ Warning: Anomaly detected in system metrics! Investigate immediately.")
        
        time.sleep(1)

    # Visualize system usage
    visualize_metrics(cpu_history, memory_history)
