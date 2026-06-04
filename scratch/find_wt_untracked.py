import os
from pathlib import Path

worktrees_dir = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\7e96b97a-cc07-41c4-91f7-a1f9fdb6f7fa\.system_generated\worktrees")

for folder in os.listdir(worktrees_dir):
    folder_path = worktrees_dir / folder
    if not folder_path.is_dir():
        continue
    print(f"\n=================== WORKTREE: {folder} ===================")
    for root, dirs, files in os.walk(folder_path):
        # Skip .git and __pycache__
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", "public", "css", "js", "images", "Image Assets"]]
        for file in files:
            # We are interested in .json, .md, .txt, .py files in scratch or root
            file_path = Path(root) / file
            rel_path = file_path.relative_to(folder_path)
            if str(rel_path).startswith("articles") or str(rel_path).endswith(".html"):
                continue
            size = file_path.stat().st_size
            print(f"  {rel_path} ({size} bytes)")
