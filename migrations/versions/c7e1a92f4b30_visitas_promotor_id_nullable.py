"""visitas.promotor_id nullable

Una visita puede registrarse sin promotor asignado (se asigna despues).
Bug 2026-08: la columna NOT NULL hacia fallar el registro de alumnos
cuando el formulario no elegia promotor, con rollback silencioso.

Revision ID: c7e1a92f4b30
Revises: 53ea819ab516
Create Date: 2026-08-20
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c7e1a92f4b30'
down_revision = '53ea819ab516'
branch_labels = None
depends_on = None


def upgrade():
    # batch_alter_table funciona en MySQL/MariaDB y en SQLite (recrea tabla)
    with op.batch_alter_table('visitas') as batch_op:
        batch_op.alter_column('promotor_id', existing_type=sa.Integer(), nullable=True)


def downgrade():
    with op.batch_alter_table('visitas') as batch_op:
        batch_op.alter_column('promotor_id', existing_type=sa.Integer(), nullable=False)
