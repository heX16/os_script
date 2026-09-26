#!/usr/bin/env python3
"""Strip FUNCTION/END_FUNCTION wrapper and (* *) comments from .st files."""

import re
from pathlib import Path

INPUT = Path(__file__).with_name('autocrane_config (PLC 2. IP-202).st')
OUTPUT = Path(__file__).with_name('autocrane_config (PLC 2. IP-202).cleaned.st')

RE_FUNCTION_LINE = re.compile(
    r'^\s*FUNCTION\s+Autocrane_Config_ST_File\b.*$',
    re.MULTILINE,
)
RE_END_FUNCTION = re.compile(r'^\s*END_FUNCTION\s*$', re.MULTILINE)
RE_PAREN_COMMENT = re.compile(r'\(\*.*?\*\)', re.DOTALL)


def strip_st(text: str) -> str:
    text = RE_FUNCTION_LINE.sub('', text)
    text = RE_END_FUNCTION.sub('', text)
    text = RE_PAREN_COMMENT.sub('', text)
    return text


def main() -> None:
    src = INPUT.read_text(encoding='utf-8')
    OUTPUT.write_text(strip_st(src), encoding='utf-8')
    print(f'Wrote: {OUTPUT}')


if __name__ == '__main__':
    main()
