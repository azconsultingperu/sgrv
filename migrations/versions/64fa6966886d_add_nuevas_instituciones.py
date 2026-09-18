"""add nuevas instituciones (10 I.E. de imagen 2026-09-15)

Revision ID: 64fa6966886d
Revises: d3c1cfee4e8e
Create Date: 2026-09-16

Fuente: MINEDU ESCALE / Identicole padrón 2026, verificado por código modular.
Todas en provincia Ascope, región La Libertad. Distrito según padrón o anexo (Licapa/La Arenita -> Paiján).
"""
from alembic import op
import sqlalchemy as sa

revision = '64fa6966886d'
down_revision = 'd3c1cfee4e8e'
branch_labels = None
depends_on = None

# Lista de 10 nuevas I.E. — ver design.md para fuentes
NUEVAS = [
    # (nombre, codigo_modular, distrito, provincia, region, tipo)
    ("I.E. 80055 Juan Ignacio Gutiérrez Fuente", "80055", "Paiján", "Ascope", "La Libertad", "Público"),
    ("I.E. José Andrés Rázuri - Pto. Chicama", None, "Rázuri", "Ascope", "La Libertad", "Público"),
    ("I.E. 80085 Miguel Grau Seminario - Macabí Alto", "80085", "Rázuri", "Ascope", "La Libertad", "Público"),  # ESCALE: Mz B Lote 10 Macabí Alto, Rázuri, Ascope
    ("I.E. Nuestra Señora de Lourdes", None, "Ascope", "Ascope", "La Libertad", "Público"),
    ("I.E. 80850 San Salvador", "80850", "Paiján", "Ascope", "La Libertad", "Público"),
    ("I.E. 80057 Inmaculada Concepción", "80057", "Chicama", "Ascope", "La Libertad", "Público"),
    ("I.E. Leoncio Prado", None, "Paiján", "Ascope", "La Libertad", "Público"),
    ("I.E. 80878 Alfonso Ugarte - Licapa", "80878", "Paiján", "Ascope", "La Libertad", "Público"),  # Licapa CP Paiján
    ("I.E. 80053 José Olaya Balandra - La Arenita", "80053", "Paiján", "Ascope", "La Libertad", "Público"),  # La Arenita CP Paiján
    ("I.E. 80050 José Félix Black", "80050", "Paiján", "Ascope", "La Libertad", "Público"),
]

def upgrade():
    conn = op.get_bind()
    # Usar bulk_insert idempotente: solo insertar si codigo_modular no existe (o nombre+distrito)
    # Para simplicidad, intentar insert y capturar duplicado via check previo
    instituciones = sa.table('instituciones_educativas',
        sa.column('nombre', sa.String),
        sa.column('distrito', sa.String),
        sa.column('provincia', sa.String),
        sa.column('region', sa.String),
        sa.column('tipo', sa.String),
        sa.column('codigo_modular', sa.String),
        sa.column('activo', sa.Boolean),
    )
    for nombre, codigo, distrito, provincia, region, tipo in NUEVAS:
        # check existe
        sel = sa.text("SELECT id FROM instituciones_educativas WHERE codigo_modular = :cm OR (codigo_modular IS NULL AND nombre = :nombre AND distrito = :distrito)")
        # En SQLite, NULL comparison necesita IS NULL, pero para códigos con valor usamos codigo_modular
        if codigo:
            res = conn.execute(sa.text("SELECT id FROM instituciones_educativas WHERE codigo_modular = :cm"), {"cm": codigo}).fetchone()
            if res:
                continue
        else:
            res = conn.execute(sa.text("SELECT id FROM instituciones_educativas WHERE nombre = :nombre AND distrito = :distrito"), {"nombre": nombre, "distrito": distrito}).fetchone()
            if res:
                continue
        op.bulk_insert(instituciones, [{
            "nombre": nombre,
            "codigo_modular": codigo,
            "distrito": distrito,
            "provincia": provincia,
            "region": region,
            "tipo": tipo,
            "activo": True,
        }])

def downgrade():
    conn = op.get_bind()
    for nombre, codigo, distrito, provincia, region, tipo in NUEVAS:
        if codigo:
            conn.execute(sa.text("DELETE FROM instituciones_educativas WHERE codigo_modular = :cm"), {"cm": codigo})
        else:
            conn.execute(sa.text("DELETE FROM instituciones_educativas WHERE nombre = :nombre AND distrito = :distrito"), {"nombre": nombre, "distrito": distrito})
