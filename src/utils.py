from .database import Database


def connect_db():
    try:
        db = Database()
        return db
    except RuntimeError as e:
        print(f"DB connect Error : {e}")
