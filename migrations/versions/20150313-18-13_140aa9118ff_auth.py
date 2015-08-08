"""auth

Revision ID: 140aa9118ff
Revises: None
Create Date: 2015-03-13 18:13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_searchable import sync_trigger


revision = '140aa9118ff'
down_revision = None


def upgrade():
    conn = op.get_bind()
    op.create_table(
        'users',
        sa.Column('name', sa.Unicode(), nullable=True),
        sa.Column('email', sa.Unicode(), nullable=True),
        sa.Column('search_vector', sa.TSVectorType(), nullable=True),
        sa.Column('locale', sa.String(length=16), nullable=True),
        sa.Column('tzinfo', sa.String(length=16), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('modified_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login', sa.Unicode(), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('last_sign_in', sa.DateTime(), nullable=True),
        sa.Column('deleted', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=True)
    sync_trigger(conn, 'users', 'search_vector', ['name', 'email'])
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'users_roles',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], [u'roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], [u'users.id'], )
    )
    op.create_index(op.f('ix_users_roles_role_id'), 'users_roles', ['role_id'], unique=False)
    op.create_index(op.f('ix_users_roles_user_id'), 'users_roles', ['user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_roles_user_id'), table_name='users_roles')
    op.drop_index(op.f('ix_users_roles_role_id'), table_name='users_roles')
    op.drop_table('users_roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
