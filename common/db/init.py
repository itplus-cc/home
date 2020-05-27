import click
from flask.cli import AppGroup
from app import database,app
import importlib,inspect
db_cli = AppGroup('db')

def getAllmodel(modules):
    clsList=[]
    for name, obj in inspect.getmembers(modules):
        if inspect.isclass(obj):
            clsList.append(obj)
    return clsList

@db_cli.command('init')
def dbinit():
    createModels=[]
    for m in app.config.get('INSTALL_MODELS',[]):
        modules=importlib.import_module(f"common.models.{m}")
        createModels+=getAllmodel(modules)
    database.create_tables(createModels,safe=True)


@db_cli.command('clear')
def dbclear():
    dropModels = []
    for m in app.config.get('INSTALL_MODELS', []):
        modules = importlib.import_module(f"common.models.{m}")
        dropModels += getAllmodel(modules)
    database.drop_tables(dropModels,safe=False)



@db_cli.command('drop')
@click.argument('module')
@click.argument('name')
def droptable(module,name):
    model = importlib.import_module(f"common.models.{module}")
    cls = getattr(model,name)
    database.drop_tables([cls],safe=False)


@db_cli.command('inittable')
@click.argument('module')
@click.argument('name')
def droptable(module,name):
    model = importlib.import_module(f"common.models.{module}")
    cls = getattr(model,name)
    database.drop_tables([cls], safe=True)
    database.create_tables([cls],safe=False)