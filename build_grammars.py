import os
import sys
from pathlib import Path

try:
    from tree_sitter import Language
    print("Tree-sitter imported successfully.")
except ImportError as e:
    print(f"Error importing tree-sitter: {e}")
    sys.exit(1)
    
grammars_dir = Path("grammars")
build_dir = Path("build")
lib_path = build_dir / "my-languages.so"

build_dir.mkdir(exist_ok=True)

python_grammar = grammars_dir / "python"
r_grammar = grammars_dir / "r"

if not python_grammar.exists():
    print(f"Error: {python_grammar} does not exist. Run: cd grammars && git clone https://github.com/tree-sitter/tree-sitter-python.git python")
    sys.exit(1)
if not r_grammar.exists():
    print(f"Error: {r_grammar} does not exist. Run: cd grammars && git clone https://github.com/r-lib/tree/sitter-r.git r")
    sys.exit(1)
    
print(f"Found Python grammar: {python_grammar}")
print(f"Found R grammar: {r_grammar}")
    

if not lib_path.exists():
    try:
        print("Building grammars...")
        Language.build_library(
            str(lib_path),
            [
                str(python_grammar),
                str(r_grammar),
            ]
        )
        print(f"Success! Built {lib_path}")
    except AttributeError as e:
        print(f"AttributeError (possible version issue): {e}")
        print("Fix: Downgrade tree-sitter to 0.20.7: pip install tree-sitter==0.20.7")
        sys.exit(1)
    except Exception as e:
        print(f"Build failed: {e}")
        print("Ensure you have a C compiler (Mac: xcode-select --install)")
        sys.exit(1)
else:
    print(f"{lib_path} already exists. Skipping build.")