import os
import sys
import re
import yaml
from pathlib import Path

def resolve_ref(base_file: Path, ref_str: str) -> bool:
    """Check if a $ref target exists and resolves properly."""
    try:
        if ref_str.startswith("#/"):
            # Internal reference check
            with open(base_file, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
            parts = ref_str.lstrip("#/").split("/")
            curr = content
            for part in parts:
                if not isinstance(curr, dict) or part not in curr:
                    return False
                curr = curr[part]
            return True
        else:
            # External file reference check (e.g. ../common/iran-banking-core.yaml#/components/schemas/NationalId)
            if "#" in ref_str:
                file_part, path_part = ref_str.split("#", 1)
            else:
                file_part, path_part = ref_str, ""
            
            target_file = (base_file.parent / file_part).resolve()
            if not target_file.exists():
                return False
            
            if path_part and path_part.startswith("/"):
                with open(target_file, "r", encoding="utf-8") as f:
                    target_content = yaml.safe_load(f)
                parts = path_part.lstrip("/").split("/")
                curr = target_content
                for part in parts:
                    if not isinstance(curr, dict) or part not in curr:
                        return False
                    curr = curr[part]
            return True
    except Exception:
        return False

def find_refs(data):
    """Recursively collect all $ref strings in a parsed YAML object."""
    refs = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == "$ref" and isinstance(v, str):
                refs.append(v)
            else:
                refs.extend(find_refs(v))
    elif isinstance(data, list):
        for item in data:
            refs.extend(find_refs(item))
    return refs

def validate_openapi_file(file_path: Path) -> list[str]:
    """Validate YAML syntax, basic OpenAPI 3 structure, and all $ref links."""
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except Exception as e:
        return [f"YAML syntax error in {file_path}: {e}"]

    if not isinstance(doc, dict):
        return [f"Root of {file_path} is not a valid YAML mapping."]

    # Check OpenAPI 3.0 basic requirements if it's a full service domain
    if "service-domains" in str(file_path):
        if "openapi" not in doc or not str(doc["openapi"]).startswith("3.0"):
            errors.append(f"{file_path.name}: Missing or invalid 'openapi: 3.0.x' version header.")
        if "info" not in doc or "title" not in doc.get("info", {}):
            errors.append(f"{file_path.name}: Missing 'info.title'.")
        if "paths" not in doc:
            errors.append(f"{file_path.name}: Missing 'paths' object.")

    # Validate all $ref links
    all_refs = find_refs(doc)
    for ref in all_refs:
        if not resolve_ref(file_path, ref):
            errors.append(f"{file_path.name}: Broken reference '$ref: {ref}'")

    return errors

def main():
    root = Path(__file__).resolve().parent.parent
    target_dir = root / "bian-iran" / "release14.0.0"
    
    if not target_dir.exists():
        print(f"Directory {target_dir} does not exist yet.")
        sys.exit(1)

    yaml_files = list(target_dir.rglob("*.yaml")) + list(target_dir.rglob("*.yml"))
    if not yaml_files:
        print(f"No YAML files found in {target_dir}.")
        sys.exit(1)

    total_errors = 0
    for yf in sorted(yaml_files):
        errs = validate_openapi_file(yf)
        if errs:
            total_errors += len(errs)
            print(f"FAIL: {yf.relative_to(root)}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS: {yf.relative_to(root)}")

    if total_errors > 0:
        print(f"\nTotal validation errors: {total_errors}")
        sys.exit(1)
    else:
        print(f"\nAll {len(yaml_files)} OpenAPI specification files passed validation successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
