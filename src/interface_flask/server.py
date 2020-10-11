import os
import textwrap

from flask import Flask, send_from_directory
import settings
from logging.config import dictConfig

import markdown2
import anon_func
import sqlalchemy

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        # 'stream': 'ext://flask.logging.wsgi_errors_stream',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


# app = Flask(__name__)

# app = Flask(__name__, root_path=os.getcwd(), template_folder="interface_flask/templates", static_folder="static")
# app = Flask(__name__, root_path=os.getcwd(), template_folder=settings['interface']['template-dir'], static_folder=settings['interface']['static-dir'])
app = Flask(__name__, root_path=os.getcwd())
app.jinja_options['extensions'].append('jinja2.ext.do')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


# import interface_flask

from interface_flask.pages import pages
from interface_flask.panes import panes, campaign, database
from interface_flask.api import api
from interface_flask.remote import remote
import db

@app.context_processor
def jinja2_values():
    import dungeonsheets

    return dict(
        settings=settings,
        campaign=campaign.current,
        int=int,
        str=str,
        list=list,
        tuple=tuple,
        type=type,
        len=len,
        dir=dir,
        getattr=getattr,
        hasattr=hasattr,
        isinstance=isinstance,
        exec=exec,
        eval=eval,
        filter=filter,
        ds=dungeonsheets,
        ordinal=lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4]),
        md=markdown2.markdown,
        db=db,
        sqltypes=sqlalchemy.sql.sqltypes,
        textwrap=textwrap,
        af=anon_func
    )

# Page endpoints:
@app.route('/blank')
def blank():
    return ""


app.register_blueprint(pages, url_prefix='/pages/')
app.register_blueprint(panes, url_prefix='/panes/')
app.register_blueprint(campaign.campaign_view, url_prefix='/panes/campaign_view')
app.register_blueprint(database.database_view, url_prefix='/panes/database_view')
app.register_blueprint(api, url_prefix='/api/')
app.register_blueprint(remote, url_prefix='/remote/')

