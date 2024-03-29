from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
import json

AWS_DB_ENDPOINT = os.getenv("AWS_DB_ENDPOINT")
AWS_DB_USERNAME = os.getenv("AWS_DB_USERNAME")
AWS_DB_PASSWORD = os.getenv("AWS_DB_PASSWORD")
AWS_DB_NAME = os.getenv("AWS_DB_NAME")
AWS_DB_PORT = os.getenv("AWS_DB_PORT")

# * Create the table in the database
engine = create_engine(f"postgresql://{AWS_DB_USERNAME}:{AWS_DB_PASSWORD}@{AWS_DB_ENDPOINT}/{AWS_DB_NAME}")
Base = declarative_base()

# * Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


# * Character table schema
class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    date_added = Column(Date)
    picture_link = Column(String)



# * Create the tables in the database
Base.metadata.create_all(engine)


def add_character_to_db(character_name, picture_link=""):
    """
    Add character to postgres characters table and return character added
    """
    new_character = Characters(full_name=character_name, date_added=datetime.date.today(),
                               picture_link=picture_link)
    session.add(new_character)
    session.commit()
    return session.query(Characters).order_by(desc(Characters.id)).first()


def handler(event, context):
    """
    Grab character name from json body and invoke add_character_to_db
    """
    body_str = event["body"]

    # Parse the JSON body
    body = json.loads(body_str)

    # Access specific fields from the body
    character = body.get("character")
    new_character = add_character_to_db(character)

    character_data = {
        "id": new_character.id,
        "name": new_character.full_name,
    }

    json_character_data = json.dumps(character_data)
    response = {
        "statusCode": 200,
        "body": f"Character has been added:\n{character_data}"
    }
    return response
