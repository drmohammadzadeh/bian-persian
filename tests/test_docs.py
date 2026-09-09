import sys
from pathlib import Path

def test_docs_exist():
    root = Path(__file__).resolve().parent.parent
    docs_dir = root / "docs"
    required_docs = [
        docs_dir / "bian-iran-lexicon.md",
        docs_dir / "cbi-regulatory-mapping.md",
        docs_dir / "bian-iran-methodology.md"
    ]
    missing = [str(d.name) for d in required_docs if not d.exists()]
    if missing:
        print(f"Missing required documentation: {', '.join(missing)}")
        sys.exit(1)
    print("All required documentation files are present.")
    sys.exit(0)

if __name__ == "__main__":
    test_docs_exist()
