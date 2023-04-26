# TODO: give IDs for which server it came from

import os

import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

#engines and permissions
CONNECTION_STRING = os.environ['CONNECTION_STRING']
engine = create_engine(CONNECTION_STRING, isolation_level="AUTOCOMMIT")

#variables


# Gets all characters and their stat block
def get_characters():
  sql = '''
    SELECT *
    FROM "characters";
    '''
  with engine.connect() as conn:
    df = pd.read_sql(sql, conn)
  return df


# Gets single character stat block
# TODO: error message doesn't print. Probably needs to be handled on main, anyway
def get_character_stats(name):
  sql = text('''
    SELECT *
    FROM "characters"
    WHERE "first_name" = :name;
    ''')
  try:
    with engine.connect() as conn:
      df = pd.read_sql(sql, conn, params={'name': name})
    return df
  except NoResultFound:
    print(
      f"Error: couldn't find {name} in character list. Please check to make sure your spelling is correct."
    )


# Add new character 
#TODO: technically they should only be adding a level 1 character. Make the default level 1. 
#TODO: Add a real error message
def add_new_character(character, server_id):
  try:
    with engine.connect() as conn:
      conn.execute(
        text('''
                INSERT INTO characters (id, first_name, last_name, skin, level, hot, cold, volatile, dark, server_id)
                VALUES (DEFAULT, :first_name, :last_name, :skin, :level, :hot, :cold, :volatile, :dark, :server_id)
            '''), character)
    return True
  except SQLAlchemyError:
    print(
      f"Error: character not created. Add something helpful for the user here"
    )
    return False
