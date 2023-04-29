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
def fetch_characters_from_db(server_id):
  sql = text("SELECT * FROM characters WHERE server_id = :server_id")
  with engine.connect() as conn:
    result = conn.execute(sql, {"server_id": str(server_id)})
    rows = result.fetchall()

  df = pd.DataFrame(rows, columns=result.keys())
  return df


# Gets single character stat block
# TODO: error message doesn't print. Probably needs to be handled on main, anyway
def get_character_stats(name, server_id):
  sql = text('''
    SELECT *
    FROM "characters"
    WHERE "first_name" = :name AND server_id = :server_id;
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
def add_new_character(character):
  try:
    with engine.connect() as conn:
      conn.execute(
        text('''
                INSERT INTO characters (first_name, last_name, skin, level, hot, cold, volatile, dark, id, server_id)
                VALUES (:first_name, :last_name, :skin, :level, :hot, :cold, :volatile, :dark, DEFAULT, :server_id)
            '''), character)
    return True
  except SQLAlchemyError:
    print("Error: character not created.")
    return False
