from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from infrastructure.models import Base

# sample DB_URL 'mysql+pymysql://unittest_root:unittest_pwd@localhost/dev_metrics'


DB_URL = os.getenv('DB_URL', 'sqlite:///dev_metrics.db')
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


class BaseRepository:

    def __init__(self):
        self.session = Session()

    def add_item(self, item):
        try:
            self.session.add(item)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

        self.session.commit()

    def add_all_items(self, items):
        try:
            self.session.add_all(items)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
