__license__ = "MIT"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inrae.fr>"


import subprocess
import sys
import os


def _run_natt(args):
    # print('== ', 'natt', ' '.join(args))
    return subprocess.run([sys.executable, '-m', 'natt']+args).returncode


def _get_datafile(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)


def test_version():
    assert _run_natt(['--version']) == 0


def test_no_arg():
    assert _run_natt([]) != 0


def test_no_path():
    assert _run_natt(['--board=week', '--date=2023-04-05']) != 0


def test_week_1():
    assert _run_natt(['--board=week', '--date=2023-04-05', _get_datafile('natt_test.ods')]) == 0


def test_week_2():
    assert _run_natt(['--board=week', '--date=2023-04-13', _get_datafile('natt_test.ods')]) == 0


def test_year():
    assert _run_natt(['--board=year', '--date=2023-04-05', _get_datafile('natt_test.ods')]) == 0
