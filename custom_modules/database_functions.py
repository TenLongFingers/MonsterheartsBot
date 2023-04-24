import os

import pandas as pd
from sqlalchemy import create_engine

CONNECTION_STRING = os.environ['CONNECTION_STRING']

engine = create_engine(CONNECTION_STRING, pool_pre_ping=True)


#gets all characters
def get_characters():
  sql = '''
    SELECT *
    FROM "characters";
    '''
  with engine.connect() as conn:
    df = pd.read_sql(sql, conn)
  return df


def get_character_single(name):
  sql = f'''
  SELECT *
  FROM "characters"
  WHERE {name} = first_name;
  '''
  with engine.connect() as conn:
    df = pd.read_sql(sql, conn)
  return df
