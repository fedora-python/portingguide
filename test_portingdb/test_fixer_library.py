from pathlib import Path
import subprocess
import re
import sys

import pytest
import modernize

basepath = Path(__file__).parent.parent / 'source'
all_rst_files = [str(p.relative_to(basepath))
                 for p in basepath.glob('**/*.rst')]

# Fixer names are in the format "<module>.fixes.fix_<name>"
FIXER_RE = re.compile(r'\w+\.fixes\.fix_\w+')


@pytest.fixture(scope='module')
def fixer_names():
    """Get list of available fixers"""
    # use subprocess -- modernize doesn't have public fixer list API
    proc = subprocess.run([sys.executable, '-m', 'modernize', '-l'],
                          stdout=subprocess.PIPE, encoding='ascii', check=True)
    lines = proc.stdout.splitlines()

    # first line is a header, all others should be fixers
    assert not FIXER_RE.fullmatch(lines[0])
    fixers = lines[1:]
    assert all([FIXER_RE.fullmatch(f) for f in fixers])

    return fixers


@pytest.mark.parametrize('filename', all_rst_files)
def test_fixers_exist(filename, fixer_names):
    """Test that all mentioned fixers are correctly named and available"""
    path = basepath / filename
    with path.open() as f:
        for lineno, line in enumerate(f, start=1):
            for match in FIXER_RE.finditer(line):
                found_text = match.group(0)
                print(f'{filename}:{lineno}:{line.strip()}')
                assert found_text in fixer_names
