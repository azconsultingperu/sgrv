# -*- coding: utf-8 -*-
"""
Bus de eventos de dominio síncrono en memoria.

Contrato (spec domain-events):
- publish(event) entrega en orden de suscripción, sin broker externo.
- Si se usa dentro de UnitOfWork, los eventos se encolan y se despachan solo en commit.
- Handlers aislados: excepción en uno no bloquea los demás ni revierte commit.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, List, Type
from collections import defaultdict

from app.utils.time_utils import peru_now

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    occurred_at: object = field(default_factory=peru_now)
    actor_id: int | None = None

    @property
    def event_type(self) -> str:
        return self.__class__.__name__

    def to_dict(self) -> dict:
        d = asdict(self)
        d["event_type"] = self.event_type
        return d


# ── Catálogo inicial (spec) ────────────────────────────────────────────
@dataclass(frozen=True, kw_only=True)
class AlumnoRegistrado(DomainEvent):
    alumno_id: int
    dni: str
    nombres: str
    apellidos: str


@dataclass(frozen=True, kw_only=True)
class AlumnoEliminado(DomainEvent):
    alumno_id: int
    dni: str


@dataclass(frozen=True, kw_only=True)
class AlumnoActualizado(DomainEvent):
    alumno_id: int
    dni: str


@dataclass(frozen=True, kw_only=True)
class UsuarioCreado(DomainEvent):
    usuario_id: int
    username: str
    dni: str


@dataclass(frozen=True, kw_only=True)
class UsuarioEliminado(DomainEvent):
    usuario_id: int
    username: str


@dataclass(frozen=True, kw_only=True)
class AvatarActualizado(DomainEvent):
    usuario_id: int
    avatar: str | None


@dataclass(frozen=True, kw_only=True)
class AvatarEliminado(DomainEvent):
    usuario_id: int


# ── Bus ────────────────────────────────────────────────────────────────
class EventBus:
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable):
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: Type[DomainEvent], handler: Callable):
        if handler in self._handlers.get(event_type, []):
            self._handlers[event_type].remove(handler)

    def clear(self):
        self._handlers.clear()

    def publish(self, event: DomainEvent):
        handlers = list(self._handlers.get(type(event), []))
        for h in handlers:
            try:
                h(event)
            except Exception as e:
                logger.exception("Event handler %s failed for %s: %s", getattr(h, "__name__", h), event.event_type, e)


# Singleton global
bus = EventBus()


def publish(event: DomainEvent):
    """Atajo para bus.publish(event). Si hay UoW activo con pending, el caller debe usar UoW.publish en su lugar."""
    bus.publish(event)


def subscribe(event_type: Type[DomainEvent], handler: Callable):
    bus.subscribe(event_type, handler)


def clear():
    bus.clear()
