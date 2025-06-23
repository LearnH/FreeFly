from celery import shared_task
from django.contrib.contenttypes.models import ContentType

from fly import models as fly_models
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def async_log_audit(
    user_id,
    content_type_app_label,
    content_type_model,
    object_id,
    action,
    ip=None,
    user_agent=None
):
    try:
        user = User.objects.get(id=user_id) if user_id else None
        content_type = ContentType.objects.get_by_natural_key(content_type_app_label, content_type_model)
        fly_models.AuditLog.objects.create(
            user=user,
            action=action,
            content_type=content_type,
            object_id=object_id,
            ip=ip,
            user_agent=user_agent
        )
    except Exception as e:
        # 建议记录异常日志（可集成 logging）
        print(f"Error creating audit log: {e}")