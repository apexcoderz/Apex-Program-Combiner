#!/usr/bin/env python3
"""
Combines source code files into a single Markdown file for review or documentation.
Created with enhancements by apexcoderz
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Iterable

# Configure logging for professional CLI output
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Supported extensions mapped to Markdown language identifiers
LANGUAGE_MAP = {
    '.ino': 'cpp', '.c': 'c', '.cpp': 'cpp',
    '.h': 'cpp', '.html': 'html', '.py': 'python'
}

def get_code_block_language(extension: str) -> str:
    """Returns the Markdown language identifier for a given file extension."""
    return LANGUAGE_MAP.get(extension.lower(), 'text')

def find_files(folder: Path, recursive: bool) -> Iterable[Path]:
    """Yields matching files from the directory tree."""
    extensions = LANGUAGE_MAP.keys()
    for ext in extensions:
        pattern = f'*{ext}'
        # Use rglob for recursive, glob for shallow search
        paths = folder.rglob(pattern) if recursive else folder.glob(pattern)
        yield from paths

def combine_files(folder_path: Path, output_file: str, recursive: bool) -> bool:
    """Reads target files and concatenates them into a formatted Markdown file."""
    if not folder_path.is_dir():
        logging.error(f"Directory not found: {folder_path}")
        return False
    
    # Sort to ensure deterministic output order
    files = sorted(find_files(folder_path, recursive))
    if not files:
        logging.warning(f"No matching files found in {folder_path}.")
        return False
    
    output_path = folder_path / output_file
    
    try:
        with output_path.open('w', encoding='utf-8') as out:
            # Add watermark header
            out.write("<!-- Generated with apexcoderz Code Combiner -->\n\n")
            
            for file_path in files:
                # Primary UTF-8 attempt, fallback to latin-1 for legacy file compatibility
                try:
                    content = file_path.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    content = file_path.read_text(encoding='latin-1')
                
                # Calculate relative path for documentation headers
                rel_path = file_path.relative_to(folder_path)
                lang = get_code_block_language(file_path.suffix)
                out.write(f"## {rel_path}\n```{lang}\n{content}")
                # Ensure code block ends cleanly
                if not content.endswith('\n'):
                    out.write('\n')
                out.write("```\n\n")
        
        logging.info(f"Combined {len(files)} files into {output_path}")
        return True
    except IOError as e:
        logging.error(f"File operation failed: {e}")
        return False

def main() -> None:
    """CLI entry point utilizing argparse for robust flag handling."""
    parser = argparse.ArgumentParser(
        description="Combine source files into a Markdown document.",
        epilog="Built with apexcoderz enhancements"
    )
    parser.add_argument("folder", type=Path, help="Target directory containing source files")
    parser.add_argument("-o", "--output", default="program.md", help="Output filename (default: program.md)")
    parser.add_argument("--no-recursive", action="store_true", help="Disable recursive search in subdirectories")
    
    args = parser.parse_args()
    
    success = combine_files(args.folder, args.output, not args.no_recursive)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
