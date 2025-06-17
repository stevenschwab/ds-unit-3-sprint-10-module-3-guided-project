import sqlite3
import pymongo
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get password and dbname
PASSWORD = os.getenv("MONGODB_PASSWORD")
DBNAME = os.getenv("MONGODB_NAME")

test_characters = [
    (1, 'Aliquid iste optio reiciendi', 0, 0, 10, 1, 1, 1, 1), 
    (2, 'Optio dolorem ex a', 0, 0, 10, 1, 1, 1, 1)
]

# Open connection to Mongo
def create_mdb_conn(password, dbname, collection_name):
    client = pymongo.MongoClient("mongodb+srv://stevenschwab1:{}@ds-unit-3-sprint-10-mod.pxenxpb.mongodb.net/{}?retryWrites=true&w=majority&appName=ds-unit-3-sprint-10-module-3".format(password, dbname))
    # db we want to connect to
    db = client[DBNAME]
    # create the collection so that we can insert into it
    collection = db[collection_name]
    return db

# create a document and insert into mongo
def char_doc_creation(mongo_db, character_list):
    for char in character_list:
        character_doc = {
            'name': char[1],
            'level': char[2],
            'exp': char[3],
            'hp': char[4],
            'strength': char[5],
            'intelligence': char[6],
            'dexterity': char[7],
            'wisdom': char[8]
        }
        mongo_db.characters.insert_one(character_doc)

# connect to sqlite
def create_sl_conn(source_db='rpg_db.sqlite3'):
    sl_conn = sqlite3.connect(source_db)
    return sl_conn

# execute a sqlite query
def execute_query(curs, query):
    return curs.execute(query).fetchall()

get_characters = """
    SELECT * FROM charactercreator_character;
"""

if __name__ == '__main__':
    # mongo connection
    db = create_mdb_conn(PASSWORD, DBNAME, 'characters')
    # print(db)

    # test doc creation
    # char_doc_creation(db, test_characters)

    # sqlite connection
    sl_conn = create_sl_conn()
    sl_curs = sl_conn.cursor()

    # get characters from sqlite
    characters = execute_query(sl_curs, get_characters)

    # create documents in mongo
    char_doc_creation(db, characters)