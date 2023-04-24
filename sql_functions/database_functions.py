import os

import pandas as pd
from sqlalchemy import create_engine

CONNECTION_STRING = os.environ['CONNECTION_STRING']

engine = create_engine(CONNECTION_STRING, pool_pre_ping=True)


def get_characters_all():
  sql = '''
    SELECT *
    FROM "characters";
    '''
  with engine.connect() as conn:
    df = pd.read_sql(sql, conn)
  return df
