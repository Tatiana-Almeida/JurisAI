from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_file(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding='utf-8')


def test_seed_initial_does_not_use_starter_plan_default():
    content = read_file('accounts/management/commands/seed_initial.py')

    assert "default='starter'" not in content
    assert "default='free'" in content


def test_seed_demo_does_not_create_organization_with_starter_plan():
    content = read_file('accounts/management/commands/seed_demo.py')

    assert "'plan': 'starter'" not in content
    assert "'plan': 'free'" in content
