# shim legacy - re-export desde módulo notifications (canónico)
from app.modules.notifications.infrastructure.email_adapter import (  # noqa: F401
    enviar_correo,
    notificar_nuevo_registro,
    notificar_nuevo_usuario,
    enviar_correo_recuperacion,
)
