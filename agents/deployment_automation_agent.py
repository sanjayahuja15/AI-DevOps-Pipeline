import subprocess
import time
import re
import numpy as np
from sklearn.ensemble import IsolationForest

# Failure history storage
failure_history = []

# Function to scan container image for vulnerabilities
def scan_container_image(image_name):
    print(f"\n🔍 Scanning container image: {image_name} for vulnerabilities...")

    # Run Trivy to scan the image
    result = subprocess.run(["trivy", "image", "--severity", "CRITICAL", image_name], capture_output=True, text=True)
    scan_output = result.stdout + result.stderr

    # Extract CRITICAL vulnerability count
    critical_match = re.search(r"CRITICAL:\s(\d+)", scan_output)
    critical_count = int(critical_match.group(1)) if critical_match else 0

    if critical_count > 0:
        print(f"🚨 {critical_count} CRITICAL vulnerabilities detected! Deployment stopped.")
        print(scan_output)  # Show Trivy output for debugging
        return False  # Stop deployment
    else:
        print("✅ No CRITICAL vulnerabilities found. Proceeding with deployment...")
        return True  # Continue deployment

# Function to check deployment status
def check_deployment_status():
    result = subprocess.run(["kubectl", "get", "pods"], capture_output=True, text=True)
    
    if "CrashLoopBackOff" in result.stdout or "ErrImagePull" in result.stdout or "ImagePullBackOff" in result.stdout:
        print("❌ Deployment Failed: Issue detected in Kubernetes pods.")
        return False
    return True

# Function to learn from past failures
def analyze_failures():
    global failure_history
    if len(failure_history) < 5:
        return False  # Not enough data to detect patterns

    clf = IsolationForest(contamination=0.2)  # Detect anomalies in failures
    clf.fit(np.array(failure_history).reshape(-1, 1))
    return clf.predict([[failure_history[-1]]])[0] == -1  # Return True if anomaly detected

# Function to perform rollback
def rollback():
    print("🚨 Rolling back deployment...")
    subprocess.run(["bash", "../scripts/rollback.sh"])
    print("✅ Rollback completed. Deployment reverted.")

if __name__ == "__main__":
    print("\n=== AI-Powered Deployment Agent Running ===")

    # Define the container image name
    container_image = "flask-webapp1:latest"

    # Run security scan
    security_check_passed = scan_container_image(container_image)

    # Stop deployment if CRITICAL vulnerabilities are found
    if not security_check_passed:
        print("❌ Deployment halted due to security risks.")
        exit(1)

    failure_count = 0
    max_failures = 3  # Threshold before rollback is triggered

    for i in range(10):  # Monitor for 10 iterations (adjust as needed)
        time.sleep(5)
        success = check_deployment_status()

        if not success:
            failure_count += 1
            failure_history.append(failure_count)
            print(f"⚠ Warning: Deployment failure detected! (Failure #{failure_count})")

        if failure_count >= max_failures:
            print("❌ Failure threshold exceeded! Triggering rollback...")
            rollback()
            break

        if analyze_failures():
            print("⚠ AI detected an unusual failure pattern! Rolling back to prevent issues.")
            rollback()
            break

    print("✅ Deployment Monitoring Complete.")
