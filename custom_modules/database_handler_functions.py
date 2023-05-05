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
def character_list_handler(server_id):
  sql = text("SELECT * FROM characters WHERE server_id = :server_id")
  with engine.connect() as conn:
    result = conn.execute(sql, {"server_id": str(server_id)})
    rows = result.fetchall()

  df = pd.DataFrame(rows, columns=result.keys())
  return df


# Gets single character stat block
def character_sheet_handler(name, server_id):
  sql = text(
    "SELECT first_name, last_name, skin, hot, cold, volatile, dark, level FROM characters WHERE first_name = :name AND server_id = :server_id"
  )
  try:
    with engine.connect() as conn:
      df = conn.execute(sql, {
        "name": name,
        "server_id": str(server_id)
      }).fetchall()

    if not df:
      return None

    return pd.DataFrame(df,
                        columns=[
                          "first_name", "last_name", "skin", "hot", "cold",
                          "volatile", "dark", "level"
                        ])

  except NoResultFound:
    return None


# Add new character
#TODO: technically they should only be adding a level 1 character. Make the default level 1.
def new_character_handler(character):
  sql = '''
                INSERT INTO characters (first_name, last_name, skin, level, hot, cold, volatile, dark, id, server_id)
                VALUES (:first_name, :last_name, :skin, :level, :hot, :cold, :volatile, :dark, DEFAULT, :server_id)
            '''
  try:
    with engine.connect() as conn:
      conn.execute(text(sql), character)
      print(sql)
    return True
  except SQLAlchemyError:
    print("Error: character not created.")
    return False


# Delete character and their associated conditions
def delete_character_handler(name, server_id):
  try:
    with engine.connect() as conn:
      # Find the character's ID
      sql_select = text(
        "SELECT id FROM characters WHERE server_id = :server_id AND first_name = :name"
      )
      result_select = conn.execute(sql_select, {
        "name": name,
        "server_id": str(server_id)
      })
      character_id = result_select.fetchone()
      if character_id is None:
        return False

      # Delete the character and their associated conditions
      sql_delete = text('''DELETE FROM conditions WHERE id = :id; \
                DELETE FROM characters WHERE id = :id;''')
      result_delete = conn.execute(sql_delete, {"id": character_id[0]})

      if result_delete.rowcount > 0:
        return True
      else:
        return False
  except SQLAlchemyError:
    print("Error: character not deleted ", sql_delete, sql_select, name,
          server_id, character_id, character_id[0])
    return False


# add condition
def add_condition_handler(name, server_id, condition):
  try:
    # get character id
    with engine.connect() as conn:
      result = conn.execute(
        text(
          "SELECT id FROM characters WHERE first_name = :name AND server_id = :server_id"
        ), {
          "name": name,
          "server_id": server_id
        })
      character_id = result.scalar()

    # insert condition
    with engine.connect() as conn:
      conn.execute(
        text(
          "INSERT INTO conditions (id, condition) VALUES (:character_id, :condition)"
        ), {
          "character_id": character_id,
          "condition": condition.capitalize()
        })
    return True
  except SQLAlchemyError:
    print(
      f'''Error: Condition not added. Here's what the database_functions module tried to push to the database:\n \n \n name = {name} \n character_id = {character_id} \n id = {id} \n server_id = {server_id} \n condition = {condition}'''
    )
    return False


#get conditions
def get_conditions_handler(name, server_id):
  with engine.connect() as conn:
    result = conn.execute(
      text(
        "SELECT characters.id, first_name, last_name FROM characters "
        "JOIN conditions "
        "ON characters.id = conditions.id "
        "WHERE characters.first_name = :name AND characters.server_id = :server_id "
      ), {
        "name": name,
        "server_id": server_id
      })
    rows = result.fetchall()
    if rows:
      conditions_arr = []
      for row in rows:
        id, first_name, last_name = row
        if id not in conditions_arr:
          conditions_arr.append(id)
      # extract conditions
      conditions = []
      for condition_id in conditions_arr:
        sql = text("SELECT condition FROM conditions WHERE id = :id")
        with engine.connect() as conn:
          result = conn.execute(sql, {"id": condition_id})
          for row in result:
            conditions.append(row[0])
      return (first_name, last_name, conditions, True)
    else:
      return (None, None, None, False)
