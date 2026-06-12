# Source Combiner CLI
A robust Python utility that aggregates source code files (`.c`, `.cpp`, `.h`, `.ino`, `.py`, `.html`) from a target directory into a single, formatted Markdown document. Ideal for passing context to LLMs, code reviews, or generating project documentation.

## Architecture/Workflow
1. **Directory Traversal:** Scans target paths recursively or shallowly using `pathlib`.
2. **File Processing:** Reads files with UTF-8 support (Latin-1 fallback).
3. **Markdown Generation:** Wraps content in syntax-highlighted Markdown code blocks with relative file path headers.

## Installation
No external dependencies required. Requires Python 3.6+.
```bash
git clone https://github.com/apexcoderz/Apex-Program-Combiner.git
cd Apex-Program-Combiner
chmod +x combine_files_apex.py
```

## Usage
```bash
# Standard recursive combination
python combine_files_apex.py ./my_project

# Specify custom output file
python combine_files_apex.py ./my_project -o combined.md

# Disable recursive search
python combine_files_apex.py ./my_project --no-recursive

```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-extension`).
3. Commit changes using Semantic Commit messages.
4. Push and open a Pull Request.
```

#### Directory Structure
```text
source-combiner/
├── .git/
├── .gitignore
├── LICENSE
├── README.md
└── src/
    └── combine_files.py
```

#### Semantic Commit Guidelines
* **`refactor: replace sys.argv with argparse module`** (Implementation of robust CLI flag handling).
* **`feat: add python 3 type hints for static analysis`** (Enhancing code maintainability).
* **`fix: correct file encoding fallback logic`** (Addressing `UnicodeDecodeError` scenarios).

#### License Recommendation
**MIT License**
*Justification:* This is a lightweight, non-proprietary utility tool. The MIT License encourages maximum open-source adoption, allowing users to freely integrate, modify, and distribute the script within both open and closed-source projects without legal friction.
