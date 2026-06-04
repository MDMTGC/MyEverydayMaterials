import json
from pathlib import Path

log_file = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\6c919d5f-e04f-474e-a60f-706d4ff23cd1\.system_generated\logs\transcript.jsonl")

if log_file.exists():
    with open(log_file, "r", encoding="utf-8") as f:
        steps = [json.loads(line) for line in f if line.strip()]
        
    print(f"Total steps in log: {len(steps)}")
    
    # Check for any tool calls that modify files
    for idx, s in enumerate(steps):
        if s.get("source") == "MODEL":
            # Check for replace_file_content or write_to_file
            if "tool_calls" in s:
                for tc in s["tool_calls"]:
                    name = tc.get("name")
                    if name in ["replace_file_content", "multi_replace_file_content", "write_to_file"]:
                        print(f"Step {idx}: Call to {name} for {tc.get('args', {}).get('TargetFile')}")
                    elif name == "run_command":
                        print(f"Step {idx}: Run command: {tc.get('args', {}).get('CommandLine')}")
            
            # Print any final paragraphs where they might have summarized the links they found
            content = s.get("content", "")
            if content and ("http" in content or "mapping" in content) and idx > len(steps) - 10:
                print(f"Step {idx}: Text content (last 10 steps):")
                print(content[:1000])
                print("-" * 50)
else:
    print("Log file does not exist")
