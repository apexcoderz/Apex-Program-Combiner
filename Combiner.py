#!/usr/bin/env python3
"""
Combines all .ino, .c, .cpp, .html, .h, and .py files in a folder (including subfolders) 
into a single program.md file.
"""

import os
import sys
from pathlib import Path


def get_code_block_language(extension):
    """Return the appropriate language identifier for markdown code blocks."""
    language_map = {
        '.ino': 'cpp',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'cpp',
        '.html': 'html',
        '.py': 'python'
    }
    return language_map.get(extension, 'text')


def combine_files(folder_path, output_file='program.md', recursive=True):
    """
    Combine all relevant files in the folder into a single markdown file.
    
    Args:
        folder_path: Path to the folder containing the files
        output_file: Name of the output file (default: program.md)
        recursive: If True, search in subfolders too (default: True)
    """
    # Supported file extensions
    extensions = {'.ino', '.c', '.cpp', '.html', '.h', '.py'}
    
    # Convert to Path object
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return False
    
    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return False
    
    # Find all matching files
    files = []
    if recursive:
        # Search recursively in all subfolders
        for ext in extensions:
            files.extend(folder.rglob(f'*{ext}'))
    else:
        # Search only in the main folder
        for ext in extensions:
            files.extend(folder.glob(f'*{ext}'))
    
    # Sort files by full path for consistent output
    files = sorted(files, key=lambda x: str(x))
    
    if not files:
        print(f"No files with extensions {extensions} found in '{folder_path}'.")
        return False
    
    # Create the output file
    output_path = folder / output_file
    
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            for file_path in files:
                # Read file contents
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # Try with a different encoding if UTF-8 fails
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                
                # Get relative path from the main folder for the header
                try:
                    relative_path = file_path.relative_to(folder)
                except ValueError:
                    relative_path = file_path.name
                
                # Get the language for the code block
                language = get_code_block_language(file_path.suffix)
                
                # Write to output file
                out.write(f"## {relative_path}\n")
                out.write(f"```{language}\n")
                out.write(content)
                # Ensure content ends with a newline
                if not content.endswith('\n'):
                    out.write('\n')
                out.write("```\n\n")
        
        print(f"Successfully combined {len(files)} files into '{output_path}'")
        print(f"\nProcessed files:")
        for file_path in files:
            try:
                relative_path = file_path.relative_to(folder)
                print(f"  - {relative_path}")
            except ValueError:
                print(f"  - {file_path.name}")
        return True
        
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False


def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python combine_files.py <folder_path> [output_file] [--no-recursive]")
        print("\nExample:")
        print("  python combine_files.py ./my_project")
        print("  python combine_files.py ./my_project combined_code.md")
        print("  python combine_files.py ./my_project program.md --no-recursive")
        print("\nBy default, searches in subfolders. Use --no-recursive to search only in main folder.")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output_file = 'program.md'
    recursive = True
    
    # Parse optional arguments
    if len(sys.argv) > 2:
        if sys.argv[2] == '--no-recursive':
            recursive = False
        else:
            output_file = sys.argv[2]
    
    if len(sys.argv) > 3 and sys.argv[3] == '--no-recursive':
        recursive = False
    
    success = combine_files(folder_path, output_file, recursive)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
