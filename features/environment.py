import mongomock

from routes import create_app
from db_handler import DbHandler

def before_feature(context, feature):
    mock_client = mongomock.MongoClient("testdb")['testdb']
    db_handler = DbHandler(mock_client)
    app = create_app(db_handler)
    app.testing = True
    context.client = app.test_client()
    context.db_handler = db_handler