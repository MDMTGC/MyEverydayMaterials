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
    
    # Check git diff if it's a git repo or compare files directly
    wt_articles = wt_path / "articles"
    main_articles = main_dir / "articles"
    
    if not wt_articles.exists():
        print("No articles directory in worktree")
        continue
        
    for file in os.listdir(wt_articles):
        if file.endswith(".py"):
            wt_file = wt_articles / file
            main_file = main_articles / file
            if main_file.exists():
                if not filecmp.cmp(wt_file, main_file, shallow=False):
                    print(f"  [MODIFIED] articles/{file}")
                    # Show a brief diff or lines changed
                    with open(main_file, "r", encoding="utf-8") as f1, open(wt_file, "r", encoding="utf-8") as f2:
                        lines1 = f1.readlines()
                        lines2 = f2.readlines()
                    import difflib
                    diff = list(difflib.unified_diff(
                        lines1, lines2, 
                        fromfile=f"main/articles/{file}", 
                        tofile=f"wt/articles/{file}", 
                        n=0
                    ))
                    # Print first 20 lines of diff
                    for d in diff[:30]:
                        print(f"    {d.strip()}")
                    if len(diff) > 30:
                        print(f"    ... and {len(diff) - 30} more lines of diff")
            else:
                print(f"  [NEW] articles/{file}")
