from pathlib import Path
import subprocess
import re
import sys

import pytest

basepath = Path(__file__).parent.parent / 'source'
all_rst_files = [str(p.relative_to(basepath))
                 for p in basepath.glob('**/*.rst')]

# All future imports mentioned
FUTURE_RE = re.compile(r'from __future__ import [^\s`]+')


def try_import(line):
    cp = subprocess.run([sys.executable, '-c', line])
    return cp.returncode


@pytest.mark.parametrize('filename', all_rst_files)
def test_future_imports_work(filename):
    """Test that all mentioned future imports work"""
    path = basepath / filename
    with path.open() as f:
        for lineno, line in enumerate(f, start=1):
            for match in FUTURE_RE.finditer(line):
                found_text = match.group(0)
                print(f'{filename}:{lineno}:{found_text}')
                assert try_import(found_text) == 0
