import os
import sys
import importlib.util
from pathlib import Path

main_dir = Path(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials")
worktrees_dir = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\7e96b97a-cc07-41c4-91f7-a1f9fdb6f7fa\.system_generated\worktrees")

subagents = {
    "Kitchen_Nursery": "subagent-Kitchen-and-Nursery-Reference-Researcher-ReferenceResearcher-4d6dd001",
    "PersonalCare_Cleaning": "subagent-Personal-Care-and-Cleaning-Reference-Researcher-ReferenceResearcher-fdb1a56b",
    "Household_PetCare": "subagent-Household-and-Pet-Care-Reference-Researcher-ReferenceResearcher-aef9df8c",
    "Tech_Outdoor": "subagent-Tech-and-Outdoor-Reference-Researcher-ReferenceResearcher-57991481",
}

def load_articles(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        spec = importlib.util.spec_from_file_location("module.name", str(filepath))
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return getattr(foo, "ARTICLES", [])
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

def get_url(src):
    if isinstance(src, (list, tuple)):
        return src[1]
    elif isinstance(src, dict):
        return src.get("url") or src.get("link")
    return str(src)

def get_title(src):
    if isinstance(src, (list, tuple)):
        return src[0]
    elif isinstance(src, dict):
        return src.get("title") or src.get("name")
    return str(src)

for name, wt_folder in subagents.items():
    wt_path = worktrees_dir / wt_folder
    print(f"\n=================== WORKTREE: {name} ===================")
    if not wt_path.exists():
        print(f"Worktree folder does not exist: {wt_path}")
        continue
        
    wt_articles_dir = wt_path / "articles"
    if not wt_articles_dir.exists():
        print("No articles directory in worktree")
        continue
        
    for file in os.listdir(wt_articles_dir):
        if file.endswith(".py"):
            wt_filepath = wt_articles_dir / file
            main_filepath = main_dir / "articles" / file
            
            wt_articles = load_articles(wt_filepath)
            main_articles = load_articles(main_filepath)
            
            wt_dict = {a["slug"]: a.get("sources", []) for a in wt_articles}
            main_dict = {a["slug"]: a.get("sources", []) for a in main_articles}
            
            for slug, wt_srcs in wt_dict.items():
                m_srcs = main_dict.get(slug, [])
                for idx, wt_src in enumerate(wt_srcs):
                    if idx < len(m_srcs):
                        m_src = m_srcs[idx]
                        wt_url = get_url(wt_src)
                        m_url = get_url(m_src)
                        if wt_url != m_url:
                            print(f"  [{slug}] Source {idx+1}:")
                            print(f"    Main: {get_title(m_src)} -> {m_url}")
                            print(f"    WT:   {get_title(wt_src)} -> {wt_url}")
