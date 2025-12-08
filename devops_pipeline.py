import os
import subprocess
import re
import time
import sys
import numpy as np
from sklearn.linear_model import LinearRegression

# Ensure subprocesses print UTF-8 on Windows and other platforms
ENV = os.environ.copy()
ENV.setdefault("PYTHONIOENCODING", "utf-8")

# Configuration Constants
TEST_THRESHOLD = 1  # If failures exceed this, rollback is triggered
MAX_RETRIES = 2  # Maximum test retries
AUTO_SCALE_INTERVAL = 60  # Auto-scaling check interval in seconds

# Function to scan Docker images for vulnerabilities
def scan_container_image(image_name):
    """Use Trivy to scan the container image for vulnerabilities before deployment."""
    print(f"\n🔍 Scanning container image: {image_name} for vulnerabilities...")
    
    # Run Trivy to scan the image. If Trivy is not installed, warn and skip scanning.
    try:
        result = subprocess.run(["trivy", "image", "--severity", "CRITICAL", image_name], capture_output=True, text=True, env=ENV)
        scan_output = (result.stdout or "") + (result.stderr or "")
    except FileNotFoundError:
        print("⚠️ Trivy not found in PATH — skipping image vulnerability scan. Install Trivy to enable security scanning.")
        return True

    # Extract CRITICAL vulnerability count
    critical_match = re.search(r"CRITICAL:\s(\d+)", scan_output)
    critical_count = int(critical_match.group(1)) if critical_match else 0

    if critical_count > 0:
        print(f"🚨 {critical_count} CRITICAL vulnerabilities detected! Deployment stopped.")
        return False  # Stop deployment only if count is greater than 0
    else:
        print("✅ No CRITICAL vulnerabilities found. Proceeding with deployment...")
        return True

# Function to run shell commands
def run_command(command):
    # Run a command and return decoded stdout (utf-8, replace errors)
    result = subprocess.run(command, capture_output=True, env=ENV)
    raw = result.stdout
    if raw is None:
        return ""
    if isinstance(raw, (bytes, bytearray)):
        return raw.decode("utf-8", errors="replace")
    return str(raw)


def run_subproc(command, timeout=None):
    """Run subprocess and return (stdout_str, stderr_str, returncode). Uses UTF-8 with replacement for undecodable bytes."""
    completed = subprocess.run(command, capture_output=True, env=ENV, timeout=timeout)
    def _dec(x):
        if x is None:
            return ""
        if isinstance(x, (bytes, bytearray)):
            return x.decode("utf-8", errors="replace")
        return str(x)
    return _dec(completed.stdout), _dec(completed.stderr), completed.returncode

# AI-Powered Scaling: Monitor CPU & Adjust Replicas
def get_cpu_usage():
    """Retrieve CPU usage of pods using kubectl top pods."""
    result = run_command(["kubectl", "top", "pods"])
    cpu_usages = []

    for line in result.split("\n"):
        if "flask-webapp1" in line:
            parts = line.split()
            cpu_value = int(parts[1].replace("m", ""))  # Convert millicores to integer
            cpu_usages.append(cpu_value)

    return np.mean(cpu_usages) if cpu_usages else 0  # Return average CPU usage

def optimize_replica_count():
    """Use AI model to predict optimal replicas based on CPU usage."""
    history_data = np.array([
        [50, 1], [100, 2], [200, 3], [300, 4], [400, 5]
    ])

    cpu_data = history_data[:, 0].reshape(-1, 1)
    replica_data = history_data[:, 1]

    model = LinearRegression()
    model.fit(cpu_data, replica_data)

    current_cpu = get_cpu_usage()
    optimal_replicas = int(round(model.predict([[current_cpu]])[0]))

    return max(1, optimal_replicas)  # Ensure at least 1 replica

def apply_auto_scaling():
    """Dynamically adjust deployment replicas based on AI predictions."""
    optimal_replicas = optimize_replica_count()
    print(f"⚡ AI-Powered Scaling: Adjusting replicas to {optimal_replicas} based on CPU usage...")
    run_command(["kubectl", "scale", "deployment", "flask-webapp1", "--replicas=" + str(optimal_replicas)])

# DevOps Pipeline Stages
def run_planning_agent(requirements_file):
    print("\n=== Running Planning Agent ===")
    stdout, stderr, returncode = run_subproc([sys.executable, "agents/analyze_requirements.py", requirements_file])
    print(stdout + stderr)
    if returncode != 0:
        print("🚨 Planning agent failed. Stopping pipeline.")
        sys.exit(1)

def run_build_agent(build_log):
    print("\n=== Running Build Automation Agent ===")
    try:
        stdout, stderr, returncode = run_subproc([sys.executable, "agents/build_automation_agent.py", build_log], timeout=120)
    except subprocess.TimeoutExpired:
        print("⏳ Build Process Timed Out! Stopping pipeline.")
        sys.exit(1)

    output = stdout + stderr
    print(output)

    # First Attempt: If the build succeeds, return early
    if "Error" not in output and returncode == 0:
        print("✅ Build Completed Successfully!")
        return True  # No need to retry

    # If the first attempt failed, proceed with retries
    print("❌ Build Failed! Retrying...")

    MAX_RETRIES = 2  # Number of retries for build failures
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"🔄 Retrying Build: Attempt {attempt}/{MAX_RETRIES}")
        stdout, stderr, returncode = run_subproc([sys.executable, "agents/build_automation_agent.py", build_log])
        output = stdout + stderr
        print(output)

        if "Error" not in output and result.returncode == 0:
            print("✅ Build Successful after retry!")
            return True

    print("🚨 Build Failed after all retries. Stopping pipeline.")
    sys.exit(1)

def run_testing_agent(test_log):
    print("\n=== Running Testing Agent ===")

    for attempt in range(1, MAX_RETRIES + 2):  # Initial attempt + retries
        stdout, stderr, returncode = run_subproc([sys.executable, "agents/testing_agent.py"])
        output = stdout + stderr
        print(output)  # Display test output

        # Extract actual test results from pytest logs
        passed_tests = len(re.findall(r"(\d+) passed", output))
        failed_tests = len(re.findall(r"(\d+) failed", output))

        if failed_tests > TEST_THRESHOLD:
            print(f"\n❌ {failed_tests} test failures detected! Threshold exceeded.\n")

            if attempt <= MAX_RETRIES:
                print(f"🔄 Retrying tests... Attempt {attempt}/{MAX_RETRIES}")
                time.sleep(2)
                continue  # Retry tests

            print("\n🚨 Too many test failures! Triggering rollback...")
            return False  # Stop pipeline
        
        return True  # Success

def run_monitoring_agent(monitoring_log):
    print("\n=== Running Monitoring and Alerting Agent ===")
    stdout, stderr, returncode = run_subproc([sys.executable, "agents/monitoring_alerting_agent.py", monitoring_log])
    print(stdout + stderr)
    if returncode != 0:
        print("🚨 Monitoring agent failed. Stopping pipeline.")
        sys.exit(1)

def run_deployment_agent(deployment_script, rollback_script, tests_passed, container_image):
    print("\n=== Running Deployment Automation Agent ===")

    if tests_passed:
        # Run Security Checks
        if not scan_container_image(container_image):
            print("🚨 Security issues found! Deployment blocked.")
            sys.exit(1)  # Stop pipeline

        print("🚀 Proceeding with Deployment...")
        stdout, stderr, returncode = run_subproc([sys.executable, "agents/deployment_automation_agent.py"])
        print(stdout + stderr)
        if returncode != 0:
            print("🚨 Deployment agent failed. Stopping pipeline.")
            sys.exit(1)

        print("\n⚡ Enabling AI-Powered Auto-Scaling...")
        apply_auto_scaling()  # Apply AI-based auto-scaling

    else:
        print("🚨 Deployment Stopped! Rolling Back...")
        subprocess.run(["bash", rollback_script], env=ENV)
        sys.exit(1)

# Main DevOps Pipeline Execution
def run_pipeline():
    print("\n🚀 Starting DevOps Pipeline with AI-Powered Auto-Scaling...")

    # File Paths
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    build_log = "logs/build_logs.txt"
    test_log = "logs/test_logs.txt"
    monitoring_log = "logs/monitoring_logs.txt"
    deployment_script = "real_project/webapp/deploy.sh"
    rollback_script = "scripts/rollback.sh"
    container_image = "flask-webapp1:latest"

    # Execute pipeline stages
    run_planning_agent(requirements_file)
    run_build_agent(build_log)

    # Run tests & check for failures
    tests_passed = run_testing_agent(test_log)

    run_monitoring_agent(monitoring_log)
    scan_container_image(container_image) # Ensure security check happens before deployment
    run_deployment_agent(deployment_script, rollback_script, tests_passed, container_image)

    print("\n✅ AI-Powered DevOps Pipeline Completed Successfully!")

if __name__ == "__main__":
    run_pipeline()
