"""Add indexes used by recipe browsing and filtering.

Revision ID: 0002_add_recipe_indexes
Revises: 0001_add_favorites
"""

from alembic import op


revision = "0002_add_recipe_indexes"
down_revision = "0001_add_favorites"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_recipes_category_id", "recipes", ["category_id"])


def downgrade():
    op.drop_index("ix_recipes_category_id", table_name="recipes")
