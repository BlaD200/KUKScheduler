"""renamed subject to lesson

Revision ID: b59c5365298d
Revises: 84127ee44a89
Create Date: 2021-10-25 02:08:24.859655

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b59c5365298d'
down_revision = '84127ee44a89'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('subjects', 'lessons')
    op.alter_column('lessons', column_name='subject_id', new_column_name='lesson_id')

    op.rename_table('subject_groups', 'lesson_groups')
    op.alter_column('lesson_groups', column_name='subject_group_id', new_column_name='lesson_group_id')
    op.alter_column('lesson_groups', column_name='subject_id', new_column_name='lesson_id')


def downgrade():
    op.rename_table('lessons', 'subjects')
    op.alter_column('subjects', column_name='lesson_id', new_column_name='subject_id')

    op.rename_table('lesson_groups', 'subject_groups')
    op.alter_column('subject_groups', column_name='lesson_group_id', new_column_name='subject_group_id')
    op.alter_column('subject_groups', column_name='lesson_id', new_column_name='subject_id')
