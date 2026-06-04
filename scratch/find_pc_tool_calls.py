import json
from pathlib import Path

log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\6c919d5f-e04f-474e-a60f-706d4ff23cd1\.system_generated\logs\transcript.jsonl")

if log_file.exists():
    with open(log_file, "r", encoding="utf-8") as f:
        steps = [json.loads(line) for line in f if line.strip()]
        
    tool_counts = {}
    for idx, s in enumerate(steps):
        if "tool_calls" in s:
            for tc in s["tool_calls"]:
                name = tc.get("name")
                tool_counts[name] = tool_counts.get(name, 0) + 1
                if name in ["run_command", "replace_file_content", "multi_replace_file_content", "write_to_file"]:
                    args = tc.get('args', {})
                    cmd = args.get('CommandLine') or args.get('TargetFile')
                    print(f"Step {idx}: {name} -> {cmd}")
    print("Tool counts:", tool_counts)
else:
    print("Log file does not exist")
