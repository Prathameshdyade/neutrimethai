"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-05-03
"""
from alembic import op
import sqlalchemy as sa


revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('slug', sa.Text(), nullable=False, unique=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('currency', sa.Text(), nullable=False, server_default='INR'),
        sa.Column('quantity_info', sa.Text(), nullable=False),
        sa.Column('shelf_life', sa.Text(), nullable=False),
        sa.Column('storage_instructions', sa.Text(), nullable=False),
        sa.Column('net_carbs', sa.Text(), nullable=True),
        sa.Column('short_description', sa.Text(), nullable=False),
        sa.Column('long_description', sa.Text(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )
    op.create_index('idx_products_slug', 'products', ['slug'])
    op.create_index('idx_products_category', 'products', ['category'])
    op.create_index('idx_products_active', 'products', ['is_active'])

    op.create_table(
        'product_images',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('product_id', sa.String(length=36), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('image_url', sa.Text(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default=sa.text('false')),
    )

    op.create_table(
        'ingredients',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False, unique=True),
    )

    op.create_table(
        'product_ingredients',
        sa.Column('product_id', sa.String(length=36), sa.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('ingredient_id', sa.String(length=36), sa.ForeignKey('ingredients.id', ondelete='CASCADE'), primary_key=True),
    )

    op.create_table(
        'tags',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False, unique=True),
        sa.Column('type', sa.Text(), nullable=False),
        sa.CheckConstraint("type IN ('diet','general')", name='ck_tags_type'),
    )

    op.create_table(
        'product_tags',
        sa.Column('product_id', sa.String(length=36), sa.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', sa.String(length=36), sa.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    )

    op.create_table(
        'allergens',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False, unique=True),
    )

    op.create_table(
        'product_allergens',
        sa.Column('product_id', sa.String(length=36), sa.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('allergen_id', sa.String(length=36), sa.ForeignKey('allergens.id', ondelete='CASCADE'), primary_key=True),
    )

    op.create_table(
        'nutrition',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('product_id', sa.String(length=36), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('calories', sa.Integer(), nullable=True),
        sa.Column('protein', sa.Float(), nullable=True),
        sa.Column('carbs', sa.Float(), nullable=True),
        sa.Column('fat', sa.Float(), nullable=True),
    )

    op.create_table(
        'benefits',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('product_id', sa.String(length=36), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('type', sa.Text(), nullable=False),
        sa.CheckConstraint("type IN ('short','detailed')", name='ck_benefits_type'),
    )

    op.create_table(
        'why_choose',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('product_id', sa.String(length=36), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
    )


def downgrade():
    op.drop_table('why_choose')
    op.drop_constraint('ck_benefits_type', 'benefits', type_='check')
    op.drop_table('benefits')
    op.drop_table('nutrition')
    op.drop_table('product_allergens')
    op.drop_table('allergens')
    op.drop_table('product_tags')
    op.drop_constraint('ck_tags_type', 'tags', type_='check')
    op.drop_table('tags')
    op.drop_table('product_ingredients')
    op.drop_table('ingredients')
    op.drop_table('product_images')
    op.drop_index('idx_products_active', table_name='products')
    op.drop_index('idx_products_category', table_name='products')
    op.drop_index('idx_products_slug', table_name='products')
    op.drop_table('products')
