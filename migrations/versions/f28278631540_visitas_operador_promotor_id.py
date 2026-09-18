"""visitas.operador_promotor_id nullable FK usuarios

Permite que el Promotor Responsable de una visita sea un usuario con rol
Operador (operador-como-promotor-responsable) sin romper el FK clasico
visitas.promotor_id -> promotores.id. Invariante: a lo sumo uno de
(promotor_id, operador_promotor_id) no nulo; ambos NULL = sin asignar.
Online-safe: columna nullable sin backfill; el codigo anterior la ignora.

Revision ID: f28278631540
Revises: 64fa6966886d
Create Date: 2026-09-16
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f28278631540'
down_revision = '64fa6966886d'
branch_labels = None
depends_on = None


def upgrade():
    # batch_alter_table funciona en MySQL/MariaDB y en SQLite (recrea tabla)
    with op.batch_alter_table('visitas') as batch_op:
        batch_op.add_column(sa.Column('operador_promotor_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_visitas_operador_promotor_id_usuarios',
            'usuarios', ['operador_promotor_id'], ['id'],
        )


def downgrade():
    with op.batch_alter_table('visitas') as batch_op:
        batch_op.drop_constraint('fk_visitas_operador_promotor_id_usuarios', type_='foreignkey')
        batch_op.drop_column('operador_promotor_id')
