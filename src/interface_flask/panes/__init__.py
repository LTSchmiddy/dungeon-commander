import os

from flask import *
from settings import current, exec_dir, paths

import game

panes = Blueprint(
    'panes',
    __name__,
    root_path=exec_dir,
    template_folder=os.path.join(exec_dir, current['interface']['view-panes']['template-dir']),
    static_folder=os.path.join(exec_dir, current['interface']['view-panes']['static-dir'])
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['view-panes']['template-dir'],
    # static_folder=settings['interface']['view-panes']['static-dir']
)

from interface_flask.panes import campaign, database

# Panes
@panes.route('/', methods=['GET', 'POST'])
def main_pain():
    return ""

