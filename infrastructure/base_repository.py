from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL
from infrastructure.models import Base

# sample DB_URL 'mysql+pymysql://unittest_root:unittest_pwd@localhost/dev_metrics'


DB_URL = os.getenv('DB_URL', 'mysql+pymysql://marketplace_mainnet_writer:2m3ark3e2tplc_i2n@snet-mps-db.c13eaekk3fgz.us-east-1.rds.amazonaws.com/metrics')
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


class BaseRepository:

    def __init__(self):
        self.session = Session(autoflush=False)

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
