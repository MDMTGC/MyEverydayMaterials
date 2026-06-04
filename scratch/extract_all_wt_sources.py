import os
import re
import ast
from pathlib import Path

main_dir = Path(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials")
worktrees_dir = Path(r"C:\Users\MDMTGC\.gemini\antigravity\brain\7e96b97a-cc07-41c4-91f7-a1f9fdb6f7fa\.system_generated\worktrees")

subagents = {
    "Kitchen_Nursery": "subagent-Kitchen-and-Nursery-Reference-Researcher-ReferenceResearcher-4d6dd001",
    "PersonalCare_Cleaning": "subagent-Personal-Care-and-Cleaning-Reference-Researcher-ReferenceResearcher-fdb1a56b",
    "Household_PetCare": "subagent-Household-and-Pet-Care-Reference-Researcher-ReferenceResearcher-aef9df8c",
    "Tech_Outdoor": "subagent-Tech-and-Outdoor-Reference-Researcher-ReferenceResearcher-57991481",
}

def extract_sources_from_file(filepath):
    """
    Extracts (article_slug, source_title, source_url) from a python article module.
    We can search for the ARTICLES list.
    """
    if not os.path.exists(filepath):
        return {}
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find ARTICLES = [ ... ]
    # A simple way is to use regex to find all objects with "slug" and "sources"
    # Or find the list.
    m = re.search(r'ARTICLES\s*=\s*(\[.*\])', content, re.DOTALL)
    if not m:
        return {}
        
    articles_str = m.group(1)
    # Safely parse or evaluate using AST
    try:
        articles = ast.literal_eval(articles_str)
    except Exception as e:
        # Fallback to regex finding
        # Find matches of "slug": "..." and "sources": [ ... ]
        articles = []
        slug_matches = re.finditer(r'"slug":\s*"([^"]+)"', content)
        for sm in slug_matches:
            slug = sm.group(1)
            # Find the sources block following this slug
            start_pos = sm.end()
            sources_match = re.search(r'"sources":\s*\[(.*?)\]', content[start_pos:], re.DOTALL)
            if sources_match:
                sources_str = "[" + sources_match.group(1) + "]"
                try:
                    sources = ast.literal_eval(sources_str)
                    articles.append({"slug": slug, "sources": sources})
                except:
                    pass
        return {a["slug"]: a["sources"] for a in articles}
        
    return {a["slug"]: a["sources"] for a in articles}

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
            
            wt_sources = extract_sources_from_file(wt_filepath)
            main_sources = extract_sources_from_file(main_filepath)
            
            for slug, sources in wt_sources.items():
                m_sources = main_sources.get(slug, [])
                # Compare sources
                for idx, src in enumerate(sources):
                    if idx < len(m_sources):
                        m_src = m_sources[idx]
                        if src[1] != m_src[1]:
                            print(f"  [{slug}] Source {idx+1}:")
                            print(f"    Main: {m_src[0]} -> {m_src[1]}")
                            print(f"    WT:   {src[0]} -> {src[1]}")
