"""catalogo queda en las 10 I.E. de imagen 2026-09-18

Las 6 seed originales (San Juan, Santa Rosa, Jose Carlos Mariategui,
Divino Maestro, San Martin de Porres, Manuel Gonzales Prada) salen del
catalogo JUNTO con sus alumnos y visitas (dato de prueba autorizado por
direccion 2026-09-18). El formulario solo lista activo=true, asi que tras
esta migracion quedan exactamente las 10 I.E. de la imagen.

Revision ID: 3ee88f7d3fef
Revises: f28278631540
Create Date: 2026-09-18
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3ee88f7d3fef'
down_revision = 'f28278631540'
branch_labels = None
depends_on = None

_VIEJAS = [
    'I.E. San Juan',
    'I.E. Santa Rosa',
    'I.E. José Carlos Mariátegui',
    'I.E. Divino Maestro',
    'I.E. San Martín de Porres',
    'I.E. Manuel Gonzales Prada',
]


def upgrade():
    conn = op.get_bind()
    for nombre in _VIEJAS:
        row = conn.execute(
            sa.text('SELECT id FROM instituciones_educativas WHERE nombre = :n'),
            {'n': nombre},
        ).fetchone()
        if not row:
            continue
        iid = row[0]
        # alumnos (y sus visitas/fotos solo referencian por alumno_id) de la I.E. vieja
        alumno_ids = [
            r[0] for r in conn.execute(
                sa.text('SELECT id FROM alumnos WHERE institucion_id = :i'),
                {'i': iid},
            ).fetchall()
        ]
        for aid in alumno_ids:
            conn.execute(
                sa.text('DELETE FROM visitas WHERE alumno_id = :a'),
                {'a': aid},
            )
        if alumno_ids:
            # delete por lotes con placeholders
            params = {f'a{n}': aid for n, aid in enumerate(alumno_ids)}
            ph = ', '.join(f':a{n}' for n in range(len(alumno_ids)))
            conn.execute(
                sa.text(f'DELETE FROM alumnos WHERE id IN ({ph})'),
                params,
            )
        conn.execute(
            sa.text('DELETE FROM instituciones_educativas WHERE id = :i'),
            {'i': iid},
        )


def downgrade():
    # Sin reversa: los alumnos e I.E. eliminados no se restauran.
    pass
