import os
import difflib
from pathlib import Path

subagents = {
    "Kitchen_Nursery": "subagent-Kitchen-and-Nursery-Reference-Researcher-ReferenceResearcher-4d6dd001",
    "PersonalCare_Cleaning": "subagent-Personal-Care-and-Cleaning-Reference-Researcher-ReferenceResearcher-fdb1a56b",
    "Household_PetCare": "subagent-Household-and-Pet-Care-Reference-Researcher-ReferenceResearcher-aef9df8c",
    "Tech_Outdoor": "subagent-Tech-and-Outdoor-Reference-Researcher-ReferenceResearcher-57991481",
}

main_dir = Path(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials")
worktrees_dir = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\7e96b97a-cc07-41c4-91f7-a1f9fdb6f7fa\.system_generated\worktrees")

for name in ["PersonalCare_Cleaning", "Household_PetCare"]:
    wt_folder = subagents[name]
    wt_path = worktrees_dir / wt_folder
    print(f"\n=================== DIFFS FOR WORKTREE: {name} ===================")
    if not wt_path.exists():
        print("Does not exist")
        continue
    
    wt_articles = wt_path / "articles"
    for file in os.listdir(wt_articles):
        if file.endswith(".py"):
            wt_file = wt_articles / file
            main_file = main_dir / "articles" / file
            if main_file.exists():
                with open(main_file, "r", encoding="utf-8") as f1, open(wt_file, "r", encoding="utf-8") as f2:
                    lines1 = f1.readlines()
                    lines2 = f2.readlines()
                
                diff = list(difflib.unified_diff(
                    lines1, lines2, 
                    fromfile=f"main/articles/{file}", 
                    tofile=f"wt/articles/{file}", 
                    n=2
                ))
                
                if diff:
                    print(f"\n--- Diff in articles/{file} ---")
                    for d in diff:
                        print(d.strip())
