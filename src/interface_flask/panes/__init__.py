import os

from flask import *
from settings import current, exec_dir, paths

import game, util

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
def main_pane():
    return ""


# Campaign View Panes
@panes.route('/file_tree_dir_listing', methods=['GET', 'POST'])
def file_tree_view__dir_listing():
    path = request.form.get('path')
    if len(os.listdir(path)) == 0:
        return f"ERROR: directory '{path}' is empty"

    return render_template("components/extract_dir_listing.html", dir_list = util.get_dir_tree(path), dir_name=game.current.name)

