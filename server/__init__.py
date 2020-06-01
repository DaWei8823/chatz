from . import db
from . import commands
from . import run_server

db.create_db()
run_server.run()