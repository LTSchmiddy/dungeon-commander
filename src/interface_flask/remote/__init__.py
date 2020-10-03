import os

from flask import *
from settings import current, exec_dir, paths

import game

remote = Blueprint(
    'remote',
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
@remote.route('/character/<int:ref_num>', methods=['GET', 'POST'])
def character_sheet(ref_num: int):
    return render_template("sheets/character_page/character_viewer.html", char=game.current.loaded_chars[ref_num])

