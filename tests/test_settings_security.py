import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def run_settings_import(extra_env, cwd):
    env = os.environ.copy()
    env.update(extra_env)
    env.pop('DJANGO_SECRET_KEY', None)
    env.pop('JWT_SIGNING_KEY', None)
    env['PYTHONPATH'] = str(REPO_ROOT)

    return subprocess.run(
        [
            sys.executable,
            '-c',
            'import jurisai.settings; print("ok")',
        ],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
    )


def test_settings_require_secret_key_when_debug_is_false(tmp_path):
    result = run_settings_import(
        {
            'DJANGO_DEBUG': 'False',
            'DJANGO_USE_SQLITE': 'False',
        },
        tmp_path,
    )

    assert result.returncode != 0
    assert 'DJANGO_SECRET_KEY must be set when DEBUG=False' in result.stderr


def test_settings_allow_dev_fallback_secret_key_when_debug_is_true(tmp_path):
    result = run_settings_import(
        {
            'DJANGO_DEBUG': 'True',
            'DJANGO_USE_SQLITE': 'True',
        },
        tmp_path,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == 'ok'
