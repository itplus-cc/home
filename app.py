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
if app.config["DATABASE_TYPE"]=="mysql":
    database = pe.MySQLDatabase(app.config["DATABASE"], **app.config["DATABASE_CONF"])
if app.config["DATABASE_TYPE"]=="sqlite":
    database = pe.SqliteDatabase(app.config["SQLITE_DB"], pragmas=app.config["SQLITE_CONF"])
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
