import os

from flask import *
from settings import current, exec_dir, paths

import game

from interface_flask.panes import panes

campaign_view = Blueprint(
    'campaign_view',
    __name__,
    root_path=exec_dir,
    template_folder=os.path.join(exec_dir, current['interface']['view-panes']['template-dir']),
    static_folder=os.path.join(exec_dir, current['interface']['view-panes']['static-dir'])
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['view-panes']['template-dir'],
    # static_folder=settings['interface']['view-panes']['static-dir']
)

# General
@campaign_view.route('/get_character/<int:id>')
def get_character(id: int):
    # character_ref_id = request.form.get('id')
    # char = game.current.loaded_chars[character_ref_id]
    char = game.current.loaded_chars[id]
    # print(char.weapon_list)
    return render_template("components/character/character_view.html", char=char)

# Campaign View Panes
@campaign_view.route('/extract_dir_listing', methods=['GET', 'POST'])
def campaign_view__extract_dir_listing():
    if len(os.listdir(game.current.dir_path)) == 0:
        return f"ERROR: campaign directory '{game.current.dir_path}' is empty"

    return render_template("panes/campaign_view/components/extract_dir_listing.html", dir_list = game.current.get_dir_tree(), dir_name=game.current.name)

@campaign_view.route('/loaded_character_listing')
def campaign_view__loaded_character_listing():
    return render_template("panes/campaign_view/components/loaded_character_listing.html",
                           characters=game.current.loaded_chars)

@campaign_view.route('/components/editor_tab', methods=['GET', 'POST'])
def campaign_view__editor_tab():
    name = request.form.get('name')
    path = request.form.get('path')

    return render_template("panes/campaign_view/components/editor_tab.html", name=name, path=path)



# Editor Types:
@campaign_view.route('/editors/json_editor', methods=['GET', 'POST'])
def mod_editor__json_editor():
    name = request.form.get('name')
    path = request.form.get('path')
    return render_template("panes/campaign_view/editors/json_editor.html", name=name, path=path)


@campaign_view.route('/editors/character_editor', methods=['GET', 'POST'])
def mod_editor__character_editor():
    name = request.form.get('name')
    id_var = request.form.get('id')

    return render_template("panes/campaign_view/editors/character_editor.html", name=name, path=id_var)