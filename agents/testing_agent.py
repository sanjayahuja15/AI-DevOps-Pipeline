import subprocess
import re
import sys

# Log file path
TEST_LOG_FILE = "logs/test_logs.txt"

def run_tests():
    """Runs pytest and captures the results."""
    print("\n=== Running Tests with Pytest ===")

    try:
        # Use sys.executable to run pytest in the current Python environment
        result = subprocess.run([sys.executable, "-m", "pytest", "--tb=short", "--disable-warnings"],
                                capture_output=True, text=True)
        output = result.stdout + result.stderr

        # Save results to log file
        with open(TEST_LOG_FILE, "w") as log:
            log.write(output)

        return output
    except FileNotFoundError:
        print("🚨 Pytest is not installed or not found. Run: pip install pytest")
        sys.exit(1)

def analyze_test_results(output):
    """Extracts test results from pytest output."""
    passed_tests = re.findall(r"(\d+) passed", output)
    failed_tests = re.findall(r"(\d+) failed", output)

    total_passed = int(passed_tests[0]) if passed_tests else 0
    total_failed = int(failed_tests[0]) if failed_tests else 0

    return total_passed, total_failed

if __name__ == "__main__":
    test_output = run_tests()
    passed, failed = analyze_test_results(test_output)

    print("\n=== Test Results ===")
    print(f"✅ Total Passed: {passed}")
    print(f"❌ Total Failed: {failed}")

    if failed > 0:
        print("🚨 Test failures detected! Exiting with error.")
        sys.exit(1)
    else:
        print("✅ All tests passed successfully!")
