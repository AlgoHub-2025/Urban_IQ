import os

def read_file(filepath, max_lines=50):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > max_lines:
                return "".join(lines[:max_lines]) + "\n... (truncated)"
            return "".join(lines)
    except Exception as e:
        return f"Error reading {filepath}: {e}"

files_to_check = [
    "backend/api.py",
    "backend/main.py",
    "backend/state.py",
    "backend/graph/workflow.py",
    "backend/agents/data_agent.py",
    "backend/agents/risk_agent.py",
    "backend/agents/decision_agent.py",
    "backend/agents/explanation_agent.py",
    "frontend/package.json",
    "frontend/src/services/api.js"
]

out_lines = []
for f in files_to_check:
    full_path = os.path.join(r"e:\Lahore HackaThone", f.replace('/', os.sep))
    out_lines.append(f"--- {f} ---")
    if os.path.exists(full_path):
        out_lines.append(read_file(full_path))
    else:
        out_lines.append("FILE NOT FOUND")
    out_lines.append("\n\n")

with open(r"e:\Lahore HackaThone\audit_scan.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print("Scan complete")
