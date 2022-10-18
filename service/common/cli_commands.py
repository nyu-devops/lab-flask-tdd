"""
Flask CLI Command Extensions
"""
from service import app
from service.models import db


######################################################################
# Command to force tables to be rebuilt
# Usage:
#   flask db-create
######################################################################
@app.cli.command("db-create")
def db_create():
    """
    Recreates a local database. You probably should not use this on
    production. ;-)
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
