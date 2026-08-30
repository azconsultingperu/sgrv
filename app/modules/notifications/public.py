# -*- coding: utf-8 -*-
"""Facade pública del módulo notifications - único punto de acoplamiento cross-módulo.

Este módulo completa el layout oficial (domain/infrastructure/presentation + public.py)
y centraliza el envío de emails vía eventos de dominio. Otros módulos no deben
importar app.services.email_service directo; deben publicar AlumnoRegistrado/UsuarioCreado.
"""
# Re-export opcional del adapter para tests o uso interno vía facade
try:
    from app.modules.notifications.infrastructure.email_adapter import enviar_correo  # noqa: F401
except Exception:  # pragma: no cover - durante bootstrap inicial puede no existir
    pass
