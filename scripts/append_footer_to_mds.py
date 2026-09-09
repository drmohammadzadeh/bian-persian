"""
Script to append the author footer to all .md files in the repository.
Ensures idempotent execution (does not duplicate if already present).
"""

import os
import sys
from pathlib import Path

# Ensure UTF-8 console output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

FOOTER_TEXT = "طراحی و توسعه: alimohammadzadeh@ut.ac.ir"
FOOTER_BLOCK = f"\n\n---\n{FOOTER_TEXT}\n"

def process_md_file(file_path: Path) -> bool:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    # Check if footer is already present
    if FOOTER_TEXT in content:
        return False

    # Append footer
    new_content = content.rstrip() + FOOTER_BLOCK
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False

def main():
    md_files = list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.MD"))
    # Filter out .git folder
    md_files = [f for f in md_files if ".git" not in f.parts]

    print(f"Found {len(md_files)} markdown files in repository.")
    updated = 0
    skipped = 0

    for f in sorted(md_files):
        if process_md_file(f):
            print(f"  + Updated: {f.relative_to(ROOT)}")
            updated += 1
        else:
            print(f"  . Skipped (already present or failed): {f.relative_to(ROOT)}")
            skipped += 1

    print("\n---------------------------------------------------------")
    print(f"Summary: {updated} files updated, {skipped} files skipped.")
    print("=========================================================")

if __name__ == "__main__":
    main()
