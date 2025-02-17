import os
import re

def analyze_requirements(requirements_file):
    """
    Reads and analyzes the requirements file to extract dependencies and project needs.
    """
    requirements_file = os.path.join(os.path.dirname(__file__),"../requirements.txt")
    try:
        with open(requirements_file, "r") as file:
            content = file.readlines()

        print("\n=== Running Planning Agent ===\n")
        print("File Content:")

        dependencies = []
        tasks = []
        features = []
        deadlines = []
        tools = []

        for line in content:
            print(line.strip())

            if re.match(r'^\s*#', line) or not line.strip():
                continue  # Skip comments and empty lines

            if "==" in line:
                dependencies.append(line.strip())  # Collect dependencies

            elif "task" in line.lower():
                tasks.append(line.strip())

            elif "feature" in line.lower():
                features.append(line.strip())

            elif "deadline" in line.lower():
                deadlines.append(line.strip())

            elif "tool" in line.lower():
                tools.append(line.strip())

        print("\n=== Planning Agent Execution Complete ===")

    except FileNotFoundError:
        print("❌ Error: Requirements file not found.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

# Run if executed directly
if __name__ == "__main__":
    analyze_requirements("requirements.txt")
