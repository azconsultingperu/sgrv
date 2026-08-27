# -*- coding: utf-8 -*-
"""
Unit of Work con soporte de eventos atómicos.

Uso:
    with UnitOfWork() as uow:
        uow.publish(AlumnoRegistrado(...))
        db.session.add(alumno)
    # al salir, commit despacha eventos; si hubo excepción, rollback descarta.

También soporta publish directo sin UoW vía app.shared.events.publish.
"""
from __future__ import annotations

from app.shared.db import db
from app.shared.events import bus, DomainEvent


class UnitOfWork:
    def __init__(self):
        self._events: list[DomainEvent] = []
        self._committed = False

    def publish(self, event: DomainEvent):
        self._events.append(event)

    def commit(self):
        db.session.commit()
        self._committed = True
        # despacha después de commit, en orden, aislando errores
        pending = list(self._events)
        self._events.clear()
        for ev in pending:
            bus.publish(ev)

    def rollback(self):
        try:
            db.session.rollback()
        finally:
            self._events.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.rollback()
            return False
        try:
            self.commit()
        except Exception:
            self.rollback()
            raise
        return False
