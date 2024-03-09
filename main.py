import sys

import mongomock

from routes import create_app
from scheduler import start_scheduler
from db_handler import DbHandler

if "--test" in sys.argv:
    mock_client = mongomock.MongoClient("testdb")['testdb']
    db_handler = DbHandler(client=mock_client)
else:
    db_handler = DbHandler()

start_scheduler(db_handler)
app = create_app(db_handler)
app.run()
