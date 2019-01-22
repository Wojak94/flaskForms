"""empty message

Revision ID: 725ee58a391d
Revises: 
Create Date: 2019-01-21 21:36:09.043513

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '725ee58a391d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('idUser', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('paswd', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('idUser'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_table('surveys',
    sa.Column('idSurvey', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('idUser', sa.Integer(), nullable=True),
    sa.Column('isActive', sa.Boolean(), nullable=True),
    sa.Column('subCount', sa.Integer(), nullable=True),
    sa.Column('dueDate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['idUser'], ['users.idUser'], ),
    sa.PrimaryKeyConstraint('idSurvey')
    )
    op.create_table('questions',
    sa.Column('idQuestion', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('idSurvey', sa.Integer(), nullable=True),
    sa.Column('replyContent', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['idSurvey'], ['surveys.idSurvey'], ),
    sa.PrimaryKeyConstraint('idQuestion')
    )
    op.create_table('replies',
    sa.Column('idReply', sa.Integer(), nullable=False),
    sa.Column('idQuestion', sa.Integer(), nullable=True),
    sa.Column('reply', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['idQuestion'], ['questions.idQuestion'], ),
    sa.PrimaryKeyConstraint('idReply')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('replies')
    op.drop_table('questions')
    op.drop_table('surveys')
    op.drop_table('users')
    op.drop_table('revoked_tokens')
    # ### end Alembic commands ###