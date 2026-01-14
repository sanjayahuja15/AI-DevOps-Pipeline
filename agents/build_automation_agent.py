import sys
import re
import subprocess
import time
import matplotlib.pyplot as plt

# Function to parse build logs
def parse_build_logs(log_file):
    errors = []
    durations = []

    try:
        with open(log_file, "r") as file:
            for line in file:
                # Extract errors
                if "ERROR" in line:
                    errors.append(line.strip())

                # Extract build durations dynamically
                match = re.search(r"completed in ([\d.]+) seconds", line)
                if match:
                    durations.append(float(match.group(1)))  # Store actual duration

    except FileNotFoundError:
        print(f"⚠ Error: Log file not found at {log_file}")
        sys.exit(1)

    return errors, durations

# Function to analyze build durations
def analyze_build_durations(durations):
    if not durations:
        return None, None, None

    avg_duration = sum(durations) / len(durations)
    longest_duration = max(d for d in durations if d > 0) if any(d>0 for d in durations) else 0
    shortest_duration = min(d for d in durations if d > 0) if any(d>0 for d in durations) else 0 # Ensure no zero values

    return avg_duration, longest_duration, shortest_duration

# Function to visualize build durations (Build Number on Y-Axis)
def visualize_durations(durations):
    if not durations:
        print("⚠ No build durations available for visualization.")
        return

    # Ensure durations are valid (ignore zero or incorrect values)
    durations = [d for d in durations if d > 0]

    if not durations:
        print("⚠ No valid build durations to plot.")
        return

    # Generate build numbers starting from 1 (oldest to latest)
    build_numbers = list(range(1, len(durations) + 1))

    # Plot with Build Number on Y-Axis and Duration on X-Axis
    plt.figure(figsize=(8, 5))
    plt.scatter(durations, build_numbers, marker="o", color="b", label="Build Duration")  # Scatter Plot
    plt.plot(durations, build_numbers, linestyle="-", color="b", alpha=0.7)  # Connect Points

    plt.title("Build Duration Trends", fontsize=14)
    plt.xlabel("Duration (seconds)", fontsize=12)
    plt.ylabel("Build Number", fontsize=12)
    plt.yticks(build_numbers)  # Ensure correct Y-axis labels
    plt.grid(True, linestyle="--", alpha=0.7)

    # Show the plot
    plt.legend()
    # plt.show()  # Commented out for automated pipeline execution
    # Save plot instead of showing it
    plt.savefig('logs/build_duration_plot.png')
    print("📊 Build duration plot saved to logs/build_duration_plot.png")

# Main script logic
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠ Error: No log file provided. Usage: python3 build_automation_agent.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]

    # Start build timer
    start_time = time.time()

    # Run build command (example)
    build_command = "make build"  # Replace with actual build command
    result = subprocess.run(build_command, shell=True, capture_output=True, text=True)

    # Stop timer and calculate real duration
    end_time = time.time()
    build_duration = round(end_time - start_time, 2)  # Correctly calculates build time
    actual_duration = end_time - start_time  # Convert to seconds

    # Append the real build duration to logs
    with open(log_file, "a") as log:
        log.write(f"Build completed in {actual_duration:.3f} seconds\n")  # Use 3 decimal places

    # Parse and analyze logs
    errors, durations = parse_build_logs(log_file)

    # Print errors (Fail pipeline only if errors exist)
    if errors:
        print("\n🚨 Build Errors Detected! Stopping Pipeline.")
        print("\n".join(errors))
        sys.exit(1)  # Stop execution on error

    print("\n✅ No errors found in the logs.")

    # Analyze build durations
    print("\n📊 Build Duration Analysis:")
    if durations:
        avg_duration, longest, shortest = analyze_build_durations(durations)
        print(f"📌 Average Duration: {avg_duration:.3f} seconds")
        print(f"📌 Longest Duration: {longest:.3f} seconds")
        print(f"📌 Shortest Duration: {shortest:.3f} seconds")

        # Visualize durations
        visualize_durations(durations)
    else:
        print("⚠ No build durations found in the logs.")

    print("✅ Build Completed Successfully!")
