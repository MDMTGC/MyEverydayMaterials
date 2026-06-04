import os
from pathlib import Path

scratch_dir = Path(r"c:\Users\MDMTGC\Desktop\MyEverydayMaterials\MyEverydayMaterials\scratch")

for file in os.listdir(scratch_dir):
    if file.startswith("summary_") and file.endswith(".txt"):
        file_path = scratch_dir / file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Look for markdown table lines containing '|' and 'http'
        lines = content.split("\n")
        table_lines = []
        for line in lines:
            if line.strip().startswith("|") and "http" in line and not "Article Slug" in line and not "---" in line:
                table_lines.append(line)
        
        if len(table_lines) > 2:
            print(f"\n=================== TABLE IN {file} ===================")
            # Print first 20 lines of the table
            for tl in table_lines[:20]:
                print(tl)
            if len(table_lines) > 20:
                print(f"... and {len(table_lines) - 20} more table lines.")
