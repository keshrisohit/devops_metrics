from eralchemy import render_er
## Draw from SQLAlchemy base
from infrastructure.models import Base

render_er(Base.metadata, 'erd_from_sqlalchemy.png')

## Draw from database
render_er("sqlite:///metrics.db", 'erd_from_sqlite.png')