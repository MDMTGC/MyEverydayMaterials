import json
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
    
    # Read the transcript
    steps = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                steps.append(json.loads(line))
                
    # Search for markdown content or tools calls containing JSON-like structures
    # and print out messages that might have mappings.
    printed_something = False
    for idx, step in enumerate(steps):
        content = step.get("content", "")
        # Look for model responses that contain JSON mapping lists or research summaries
        if step.get("source") == "MODEL" and content:
            if "mapping" in content.lower() or "{" in content:
                # If there is a JSON code block, or a dictionary, let's print it
                if "```json" in content or "```" in content:
                    print(f"Step {idx}: Found code block in content:")
                    print(content[-2000:]) # Show the last 2000 chars of it
                    printed_something = True
                    break
        
    if not printed_something:
        # Just show the last model content if nothing else matched
        model_contents = [s.get("content", "") for s in steps if s.get("source") == "MODEL" and s.get("content")]
        if model_contents:
            print("Last model content:")
            print(model_contents[-1][-2000:])
