from routes import create_app
from scheduler import start_scheduler
from db_handler import DbHandler


db_handler = DbHandler()
start_scheduler(db_handler)
app = create_app(db_handler)
app.run()
