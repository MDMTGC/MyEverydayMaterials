import os
import filecmp
from pathlib import Path

subagents = {
    "Kitchen_Nursery": "subagent-Kitchen-and-Nursery-Reference-Researcher-ReferenceResearcher-4d6dd001",
    "PersonalCare_Cleaning": "subagent-Personal-Care-and-Cleaning-Reference-Researcher-ReferenceResearcher-fdb1a56b",
    "Household_PetCare": "subagent-Household-and-Pet-Care-Reference-Researcher-ReferenceResearcher-aef9df8c",
    "Tech_Outdoor": "subagent-Tech-and-Outdoor-Reference-Researcher-ReferenceResearcher-57991481",
}

main_dir = Path(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials")
worktrees_dir = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\7e96b97a-cc07-41c4-91f7-a1f9fdb6f7fa\.system_generated\worktrees")

for name, wt_folder in subagents.items():
    wt_path = worktrees_dir / wt_folder
    print(f"\n=================== WORKTREE: {name} ===================")
    if not wt_path.exists():
        print(f"Worktree folder does not exist: {wt_path}")
        continue
    
    wt_articles = wt_path / "articles"
    if not wt_articles.exists():
        print("No articles directory")
        continue
        
    for file in os.listdir(wt_articles):
        if file.endswith(".py"):
            wt_file = wt_articles / file
            main_file = main_dir / "articles" / file
            if main_file.exists():
                if not filecmp.cmp(wt_file, main_file, shallow=False):
                    print(f"  [MODIFIED] articles/{file}")
                else:
                    print(f"  [IDENTICAL] articles/{file}")
            else:
                print(f"  [NEW] articles/{file}")
