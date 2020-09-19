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

# Panes
@panes.route('/', methods=['GET', 'POST'])
def main_pain():
    return ""


# General
@panes.route('/campaign_view/get_character/<int:id>')
def get_character(id: int):
    # character_ref_id = request.form.get('id')
    # char = game.current.loaded_chars[character_ref_id]
    char = game.current.loaded_chars[id]

    return render_template("components/character/character_view.html", char=char)

# Campaign View Panes
@panes.route('/campaign_view/extract_dir_listing')
def campaign_view__extract_dir_listing():
    if len(os.listdir(game.current.dir_path)) == 0:
        return f"ERROR: campaign directory '{game.current.dir_path}' is empty"

    return render_template("panes/campaign_view/components/extract_dir_listing.html", dir_list = game.current.get_dir_tree(), dir_name=game.current.name)

@panes.route('/campaign_view/loaded_character_listing')
def campaign_view__loaded_character_listing():
    return render_template("panes/campaign_view/components/loaded_character_listing.html",
                           characters=game.current.loaded_chars)

@panes.route('/campaign_view/components/editor_tab', methods=['GET', 'POST'])
def campaign_view__editor_tab():
    name = request.form.get('name')
    path = request.form.get('path')

    return render_template("panes/campaign_view/components/editor_tab.html", name=name, path=path)



# Editor Types:
@panes.route('/campaign_view/editors/json_editor', methods=['GET', 'POST'])
def mod_editor__json_editor():
    name = request.form.get('name')
    path = request.form.get('path')
    return render_template("panes/campaign_view/editors/json_editor.html", name=name, path=path)


@panes.route('/campaign_view/editors/character_editor', methods=['GET', 'POST'])
def mod_editor__character_editor():
    name = request.form.get('name')
    id = request.form.get('id')

    return render_template("panes/campaign_view/editors/character_editor.html", name=name, path=id)