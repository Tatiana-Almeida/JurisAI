from ai_assistant.services.ai_service import PLAN_IA_LIMITS


def test_plan_ia_limits_uses_current_organization_plan_keys():
    assert 'starter' not in PLAN_IA_LIMITS
    assert PLAN_IA_LIMITS['free'] == 20
    assert PLAN_IA_LIMITS['solo'] == 100
    assert PLAN_IA_LIMITS['growth'] == 100
    assert PLAN_IA_LIMITS['enterprise'] == 2000
