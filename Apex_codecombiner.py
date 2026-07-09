#!/usr/bin/env python3
import argparse
import logging
import shutil
import sys
import time
from pathlib import Path
from typing import Iterable

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

LANGUAGE_MAP = {
    '.ino': 'cpp', '.c': 'c', '.cpp': 'cpp',
    '.h': 'cpp', '.html': 'html', '.py': 'python'
}

COLOR_RESET = "\033[0m"
COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_MAGENTA = "\033[95m"
COLOR_DIM = "\033[2m"


def supports_color() -> bool:
    return sys.stdout.isatty()


def colorize(text: str, color: str) -> str:
    return f"{color}{text}{COLOR_RESET}" if supports_color() else text

def print_banner() -> None:
    banner = r"""
    ___    ____     __________  ____  ______   _________  __  _______  _____   ____________
   /   |  / __ \   / ____/ __ \/ __ \/ ____/  / ____/ __ \/  |/  / __ )/  _/ | / / ____/ __ \
  / /| | / /_/ /  / /   / / / / / / / __/    / /   / / / / /|_/ / __  |/ //  |/ / __/ / /_/ /
 / ___ |/ ____/  / /___/ /_/ / /_/ / /___   / /___/ /_/ / /  / / /_/ // // /|  / /___/ _, _/
/_/  |_/_/       \____/\____/_____/_____/   \____/\____/_/  /_/_____/___/_/ |_/_____/_/ |_|
"""
    print(colorize(banner, COLOR_CYAN))
    print(colorize("  Source Code Combiner  ·  aditya projects.id   ·   apexcoderz ", COLOR_DIM))


def print_easter_egg() -> None:
    art = r'''
      .-""""""-.
    .'          '.
   /   O      O   \      "Code with love."
  :                 :
  |                 |     built by  apexcoderz x AP
  :    \        /   :     for       Lahbakosan
   \    '.____.'    /
    '.            .'
      '-.......-'
'''
    print(colorize(art, COLOR_MAGENTA))


def get_code_block_language(extension: str) -> str:
    return LANGUAGE_MAP.get(extension.lower(), 'text')


def find_files(folder: Path, recursive: bool) -> Iterable[Path]:
    for ext in LANGUAGE_MAP:
        pattern = f'*{ext}'
        yield from (folder.rglob(pattern) if recursive else folder.glob(pattern))


def render_progress(current: int, total: int, label: str, width: int = 30) -> None:
    ratio = current / total if total else 1
    filled = int(width * ratio)
    bar = "█" * filled + "░" * (width - filled)
    line = f"\r  [{colorize(bar, COLOR_GREEN)}] {current}/{total}  {colorize(label, COLOR_DIM)}"
    pad = max(0, shutil.get_terminal_size((80, 20)).columns - len(line) + 20)
    sys.stdout.write(line + " " * pad)
    sys.stdout.flush()
    if current == total:
        sys.stdout.write("\n")


def combine_files(folder_path: Path, output_file: str, recursive: bool) -> bool:
    if not folder_path.is_dir():
        logging.error(f"Directory not found: {folder_path}")
        return False

    files = sorted(find_files(folder_path, recursive))
    if not files:
        logging.warning(f"No matching files found in {folder_path}.")
        return False

    output_path = folder_path / output_file

    try:
        with output_path.open('w', encoding='utf-8') as out:
            out.write("<!-- Combined with Code Combiner · aditya projects.id · apexcoderz -->\n\n")

            for index, file_path in enumerate(files, start=1):
                render_progress(index, len(files), file_path.name)
                try:
                    content = file_path.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    content = file_path.read_text(encoding='latin-1')

                rel_path = file_path.relative_to(folder_path)
                lang = get_code_block_language(file_path.suffix)
                out.write(f"## {rel_path}\n```{lang}\n{content}")
                if not content.endswith('\n'):
                    out.write('\n')
                out.write("```\n\n")
                time.sleep(0.02)

        logging.info(colorize(f"Combined {len(files)} files into {output_path}", COLOR_GREEN))
        return True
    except IOError as e:
        logging.error(f"File operation failed: {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Combine source files into a single Markdown document.",
        epilog="aditya projects.id"
    )
    parser.add_argument("folder", type=Path, nargs='?', help="Target directory containing source files")
    parser.add_argument("-o", "--output", default="program.md", help="Output filename (default: program.md)")
    parser.add_argument("--no-recursive", action="store_true", help="Disable recursive search in subdirectories")
    parser.add_argument("--credits", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.credits or (args.folder and str(args.folder) in ("42", "apexcoderz", "aditya")):
        print_easter_egg()
        sys.exit(0)

    if args.folder is None:
        parser.error("the following arguments are required: folder")

    print_banner()
    success = combine_files(args.folder, args.output, not args.no_recursive)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
