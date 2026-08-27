# -*- coding: utf-8 -*-
"""Shared kernel DB instance - evita que domain importe app directamente."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
