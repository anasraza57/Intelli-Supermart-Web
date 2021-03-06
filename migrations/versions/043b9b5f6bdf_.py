"""empty message

Revision ID: 043b9b5f6bdf
Revises: 
Create Date: 2020-03-10 11:52:38.501298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '043b9b5f6bdf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('fki_invoice_customer_id_fkey', table_name='invoice')
    op.drop_index('fki_invoice_order_id_fkey', table_name='invoice')
    op.drop_table('invoice')
    op.drop_table('record')
    op.drop_table('subcategory')
    op.drop_table('cart')
    op.drop_table('inventory')
    op.drop_table('admin')
    op.drop_index('fki_order_customer_id_fkey', table_name='order')
    op.drop_index('fki_order_product_id_fkey', table_name='order')
    op.drop_table('order')
    op.drop_table('picture')
    op.drop_table('review')
    op.drop_table('customer')
    op.drop_table('category')
    op.add_column('product', sa.Column('description', sa.String(length=1000), nullable=True))
    op.alter_column('product', 'picture_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('product', 'product_description',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('product', 'product_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('product', 'product_price',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index('fki_product_subcategory_id_fkey', table_name='product')
    op.drop_constraint(u'product_picture_id_fkey', 'product', type_='foreignkey')
    op.drop_constraint(u'product_subcategory_id_fkey', 'product', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(u'product_subcategory_id_fkey', 'product', 'subcategory', ['prod_subcategory_id'], ['subcategory_id'])
    op.create_foreign_key(u'product_picture_id_fkey', 'product', 'picture', ['picture_id'], ['picture_id'])
    op.create_index('fki_product_subcategory_id_fkey', 'product', ['prod_subcategory_id'], unique=False)
    op.alter_column('product', 'product_price',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('product', 'product_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('product', 'product_description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('product', 'picture_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('product', 'description')
    op.create_table('category',
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('category_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('picture_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['picture_id'], [u'picture.picture_id'], name=u'category_picture_id_fkey'),
    sa.PrimaryKeyConstraint('category_id', name=u'category_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('customer',
    sa.Column('customer_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('customer_email', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('customer_password', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('customer_address', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('customer_age', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('customer_gender', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('customer_phone', sa.CHAR(length=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('customer_id', name=u'customer_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('review',
    sa.Column('review_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('review_stars', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('review_description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['product_id'], [u'product.product_id'], name=u'review_product_id_fkey'),
    sa.PrimaryKeyConstraint('review_id', name=u'review_pkey')
    )
    op.create_table('picture',
    sa.Column('picture_id', sa.INTEGER(), server_default=sa.text(u"nextval('picture_picture_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('picture_url', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('picture_id', name=u'picture_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('order',
    sa.Column('order_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('order_quantity', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('order_amount', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('order_status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('order_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('product_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('customer_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], [u'customer.customer_id'], name=u'order_customer_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], [u'product.product_id'], name=u'order_product_id_fkey'),
    sa.PrimaryKeyConstraint('order_id', name=u'order_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('fki_order_product_id_fkey', 'order', ['product_id'], unique=False)
    op.create_index('fki_order_customer_id_fkey', 'order', ['customer_id'], unique=False)
    op.create_table('admin',
    sa.Column('admin_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('admin_name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('admin_phone', sa.CHAR(length=11), autoincrement=False, nullable=True),
    sa.Column('admin_email', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('admin_password', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('admin_address', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('admin_id', name=u'admin_pkey')
    )
    op.create_table('inventory',
    sa.Column('product_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('product_quantity', sa.BIGINT(), autoincrement=False, nullable=True)
    )
    op.create_table('cart',
    sa.Column('cart_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_cost', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customer_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('product_quantity', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], [u'customer.customer_id'], name=u'cart_customer_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], [u'product.product_id'], name=u'cart_product_id_fkey'),
    sa.PrimaryKeyConstraint('cart_id', name=u'cart_pkey')
    )
    op.create_table('subcategory',
    sa.Column('subcategory_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subcategory_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], [u'category.category_id'], name=u'subcategory_category_id_fkey'),
    sa.PrimaryKeyConstraint('subcategory_id', name=u'subcategory_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('record',
    sa.Column('rec_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('investment', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('sale', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('profit', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('loss', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('invoice_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['invoice_id'], [u'invoice.invoice_id'], name=u'record_invoice_id_fkey'),
    sa.PrimaryKeyConstraint('rec_id', name=u'record_pkey')
    )
    op.create_table('invoice',
    sa.Column('invoice_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('order_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('customer_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('total_amount', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], [u'customer.customer_id'], name=u'invoice_customer_id_fkey'),
    sa.ForeignKeyConstraint(['order_id'], [u'order.order_id'], name=u'invoice_order_id_fkey'),
    sa.PrimaryKeyConstraint('invoice_id', name=u'invoice_pkey')
    )
    op.create_index('fki_invoice_order_id_fkey', 'invoice', ['order_id'], unique=False)
    op.create_index('fki_invoice_customer_id_fkey', 'invoice', ['customer_id'], unique=False)
    # ### end Alembic commands ###
