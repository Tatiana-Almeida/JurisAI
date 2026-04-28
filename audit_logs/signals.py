import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection, OperationalError
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from audit_logs.models import AuditLog
from jurisai.middleware import get_current_request


def should_audit_model(sender):
    app_label = getattr(sender._meta, 'app_label', '')
    if app_label in {'audit_logs', 'migrations'}:
        return False
    if app_label in {'admin', 'auth', 'contenttypes', 'sessions'}:
        return False
    return True


def is_audit_table_ready():
    try:
        return AuditLog._meta.db_table in connection.introspection.table_names()
    except OperationalError:
        return False


def serialize_for_json(value):
    if value is None:
        return None
    try:
        serialized = json.dumps(value, cls=DjangoJSONEncoder)
        return json.loads(serialized)
    except TypeError:
        return str(value)


def record_audit(instance, action, before, after):
    if not is_audit_table_ready():
        return
    request = get_current_request()
    user = getattr(request, 'user', None) if request else None
    if user is not None and not getattr(user, 'is_authenticated', False):
        user = None
    AuditLog.objects.create(
        user=user,
        action=action,
        entity=f'{instance._meta.app_label}.{instance._meta.model_name}',
        before=serialize_for_json(before),
        after=serialize_for_json(after),
        ip=getattr(request, 'META', {}).get('REMOTE_ADDR') if request else None,
    )

@receiver(pre_save)
def audit_pre_save(sender, instance, **kwargs):
    if not should_audit_model(sender):
        return
    if instance.pk:
        try:
            existing = sender.objects.get(pk=instance.pk)
            instance._audit_snapshot = model_to_dict(existing)
        except sender.DoesNotExist:
            instance._audit_snapshot = None

@receiver(post_save)
def audit_post_save(sender, instance, created, **kwargs):
    if not should_audit_model(sender):
        return
    before = getattr(instance, '_audit_snapshot', None)
    after = model_to_dict(instance)
    record_audit(instance, 'create' if created else 'update', before, after)

@receiver(post_delete)
def audit_post_delete(sender, instance, **kwargs):
    if not should_audit_model(sender):
        return
    before = model_to_dict(instance)
    record_audit(instance, 'delete', before, None)

