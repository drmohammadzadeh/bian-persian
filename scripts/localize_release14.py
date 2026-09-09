"""
BIAN Release 14.0.0 Complete Persian Localization Engine
Processes all 1040 files of release 14.0.0 and mirrors them into bian-iran/release14.0.0/
with Persian titles, descriptions, action summaries, and Central Bank of Iran system mappings.
"""

import os
import sys
import time
import shutil
import re
from pathlib import Path

# Ensure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from domain_dictionary import get_domain_info, ACTION_TRANSLATIONS

def localize_yaml_content(content: str, domain_name: str, is_async: bool) -> str:
    """Enriches YAML content with Persian metadata, titles, descriptions, and action translations."""
    info = get_domain_info(domain_name)
    fa_title = info["title"]
    fa_desc = info["description"]
    cbi_system = info["cbi_system"]

    lines = content.splitlines()
    output_lines = []
    
    in_info = False
    info_indent = 0
    info_modified = False
    description_replaced = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Track info: block
        if re.match(r'^info:\s*$', line):
            in_info = True
            output_lines.append(line)
            i += 1
            continue
            
        if in_info:
            # Check if info block ended (a new top-level key like servers:, paths:, channels:, components:)
            if re.match(r'^[a-zA-Z0-9_\-]+:\s*', line) and not line.startswith(' '):
                # Inject Persian extensions right before ending info block if not already done
                if not info_modified:
                    output_lines.append(f"  x-persian-title: '{fa_title}'")
                    output_lines.append(f"  x-persian-description: '{fa_desc}'")
                    output_lines.append(f"  x-cbi-system: '{cbi_system}'")
                    output_lines.append("  x-bian-standard: 'BIAN-Iran v14.0.0'")
                    info_modified = True
                in_info = False
                output_lines.append(line)
                i += 1
                continue
            
            # Enhance title
            title_match = re.match(r'^(\s+title:\s*[\'"]?)(.*?)([\'"]?\s*)$', line)
            if title_match:
                prefix, old_title, suffix = title_match.groups()
                clean_old = old_title.strip("'\"")
                output_lines.append(f"{prefix}{clean_old} - {fa_title}{suffix}")
                i += 1
                continue
            
            # Enhance description
            if re.match(r'^\s+description:\s*', line) and not description_replaced:
                # Capture single-line or multi-line description
                desc_match = re.match(r'^(\s+description:\s*)(.*)$', line)
                prefix = desc_match.group(1)
                first_part = desc_match.group(2).strip()
                
                # Check if it's folded scalar (>- or |)
                if first_part in ('>-', '>', '|', '|-'):
                    # Multi-line block
                    orig_desc_lines = []
                    i += 1
                    while i < len(lines) and (lines[i].startswith('    ') or lines[i].strip() == ''):
                        orig_desc_lines.append(lines[i].strip())
                        i += 1
                    orig_desc = " ".join([l for l in orig_desc_lines if l])
                    output_lines.append(f"{prefix}>-")
                    output_lines.append(f"    {fa_desc} | {orig_desc}")
                else:
                    clean_orig = first_part.strip("'\"")
                    output_lines.append(f"{prefix}>-")
                    output_lines.append(f"    {fa_desc} | {clean_orig}")
                    i += 1
                description_replaced = True
                continue

        # Outside or inside paths: translate operation summary lines
        summary_match = re.match(r'^(\s+summary:\s*)(.*)$', line)
        if summary_match:
            prefix, text = summary_match.groups()
            clean_text = text.strip("'\"")
            first_word = clean_text.split()[0] if clean_text.split() else ""
            if first_word in ACTION_TRANSLATIONS:
                fa_action = ACTION_TRANSLATIONS[first_word]
                escaped_text = clean_text.replace("'", "''")
                output_lines.append(f"{prefix}'{escaped_text} ({fa_action})'")
                i += 1
                continue

        output_lines.append(line)
        i += 1

    return "\n".join(output_lines) + "\n"

def process_directory(src_dir: Path, dst_dir: Path, is_async: bool) -> tuple[int, int]:
    """Processes all files from src_dir into dst_dir."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    yaml_count = 0
    other_count = 0
    
    for item in sorted(src_dir.iterdir()):
        if item.is_file():
            if item.suffix in ('.yaml', '.yml'):
                domain_name = item.stem
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        raw_content = f.read()
                    
                    localized = localize_yaml_content(raw_content, domain_name, is_async)
                    dst_file = dst_dir / item.name
                    with open(dst_file, 'w', encoding='utf-8') as f:
                        f.write(localized)
                    yaml_count += 1
                except Exception as e:
                    print(f"Error processing {item.name}: {e}")
            else:
                # Copy non-yaml files (e.g. Readme.md)
                dst_file = dst_dir / item.name
                shutil.copy2(item, dst_file)
                other_count += 1
                
    return yaml_count, other_count

def main():
    start_time = time.time()
    root = Path(__file__).resolve().parent.parent
    src_root = root / "release14.0.0"
    dst_root = root / "bian-iran" / "release14.0.0"
    
    if not src_root.exists():
        print(f"Source directory {src_root} not found!")
        sys.exit(1)
        
    print("=========================================================")
    print(" BIAN Release 14.0.0 Iranian Localization Pipeline")
    print("=========================================================")
    print(f"Source:      {src_root}")
    print(f"Destination: {dst_root}\n")

    targets = [
        ("semantic-apis/oas3/yamls", False),
        ("semantic-apis/asyncapi-3.x/yamls", True),
        ("apis-iso20022_ext-ddd/oas3/yamls", False),
        ("apis-iso20022_ext-ddd/asyncapi-3.x/yamls", True),
    ]

    total_yaml = 0
    total_other = 0

    for rel_path, is_async in targets:
        s_dir = src_root / rel_path
        d_dir = dst_root / rel_path
        print(f"Processing: {rel_path} ...", end=" ", flush=True)
        t0 = time.time()
        y_cnt, o_cnt = process_directory(s_dir, d_dir, is_async)
        dt = time.time() - t0
        print(f"Done! ({y_cnt} YAMLs, {o_cnt} others in {dt:.2f}s)")
        total_yaml += y_cnt
        total_other += o_cnt

    # Copy top-level release14.0.0 Readme.md if present
    if (src_root / "Readme.md").exists():
        shutil.copy2(src_root / "Readme.md", dst_root / "Readme.md")
        total_other += 1

    elapsed = time.time() - start_time
    print("\n---------------------------------------------------------")
    print(f"Localization Complete in {elapsed:.2f} seconds!")
    print(f"Total YAML files localized: {total_yaml}")
    print(f"Total auxiliary files:      {total_other}")
    print(f"Total files in bian-iran:   {total_yaml + total_other}")
    print("=========================================================")

if __name__ == "__main__":
    main()
