from flask import Flask
import os
from playhouse.flask_utils import FlaskDB
import peewee as pe
from flask_cors import CORS


app = Flask(__name__,)
env = os.environ.get("FLASK_ENV")
try:
    app.config.from_pyfile(f"config/{env}.py")
except Exception as e:
    print(f"{e.__class__.__name__}: {e}")

CORS(supports_credentials=True).init_app(app)

#database = pe.MySQLDatabase(app.config["DATABASE"], **app.config["DATABASE_CONF"])
database = pe.SqliteDatabase('my_home.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': 10000,  # 10000 pages, or ~40MB
    'foreign_keys': 1,  # Enforce foreign-key constraints
})
db = FlaskDB(app, database)
from apps import *
from common.db.init import db_cli

app.cli.add_command(db_cli)
"""
函数模板
"""
from common.libs.UrlManager import UrlManager

app.add_template_global(UrlManager.buildStaticUrl, "buildStaticUrl")
app.add_template_global(UrlManager.buildUrl, "buildUrl")

if __name__ == "__main__":
    app.run()
