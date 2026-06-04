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
    conv_path = brain_dir / conv_id
    print(f"\n=================== BRAIN FOLDER: {name} ({conv_id}) ===================")
    if not conv_path.exists():
        print("Folder does not exist")
        continue
    for root, dirs, files in os.walk(conv_path):
        # Skip .system_generated
        dirs[:] = [d for d in dirs if d != ".system_generated"]
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(conv_path)
            size = file_path.stat().st_size
            print(f"  {rel_path} ({size} bytes)")
