import os

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

CONNECTION_STRING = os.environ['CONNECTION_STRING']

engine = create_engine(CONNECTION_STRING, pool_pre_ping=True)


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
        print(f"Error: couldn't find {name} in character list. Please check to make sure your spelling is correct.")


# Add new character
def add_new_character(character):
    try:
        with engine.connect() as conn:
            conn.execute(text('''
                INSERT INTO characters (first_name, last_name, skin, level, hot, cold, volatile, dark)
                VALUES (:first_name, :last_name, :skin, :level, :hot, :cold, :volatile, :dark)
            '''), character)
        return True
    except SQLAlchemyError:
        print(f"Error: couldn't find {character['first_name']} in character list. Please check to make sure your spelling is correct.")
        return False

