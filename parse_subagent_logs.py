import json
import os
from pathlib import Path

subagents = {
    "Kitchen_Nursery": "71730ed9-f117-4b0b-8c98-01469c547bff",
    "PersonalCare_Cleaning": "6c919d5f-e04f-474e-a60f-706d4ff23cd1",
    "Household_PetCare": "b904725a-cefe-4bc9-b7cd-867ac94b7dec",
    "Tech_Outdoor": "be3fdaf6-a958-477a-9e0c-2cc4ee1e31ec",
}

brain_dir = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain")

for name, conv_id in subagents.items():
    log_file = brain_dir / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
    print(f"\n=================== SUBAGENT: {name} ({conv_id}) ===================")
    if not log_file.exists():
        print(f"Log file does not exist: {log_file}")
        continue
    
    # Let's find the last few steps and messages
    steps = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                steps.append(json.loads(line))
    
    print(f"Total steps: {len(steps)}")
    # Find any send_message tool calls or model responses that look like final outputs
    messages_sent = []
    for step in steps:
        if step.get("source") == "MODEL" and "tool_calls" in step:
            for tc in step["tool_calls"]:
                if tc.get("name") == "send_message":
                    messages_sent.append(tc.get("args"))
                    
    if messages_sent:
        print(f"Found {len(messages_sent)} send_message calls. Last one:")
        last_msg = messages_sent[-1]
        print(json.dumps(last_msg, indent=2))
    else:
        print("No send_message calls found.")
        # Print the last model text content
        model_texts = [s for s in steps if s.get("source") == "MODEL" and s.get("content")]
        if model_texts:
            print("Last model response content:")
            print(model_texts[-1]["content"][:1000])
