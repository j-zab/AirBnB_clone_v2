#!/usr/bin/python3
""" Initialize the models package """

from os import getenv
from models.engine import file_storage
from models.engine import db_storage

# Check the value of HBNB_TYPE_STORAGE environment variable
storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = file_storage.FileStorage()

# Load the storage data
storage.reload()
