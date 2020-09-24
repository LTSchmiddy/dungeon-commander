import os

from flask import *
from settings import current, exec_dir, paths

from sqlalchemy.sql.schema import Table, Column

import dungeonsheets
import db

# import game
# from interface_flask.panes import panes



database_view = Blueprint(
    'database',
    __name__,
    root_path=exec_dir,
    template_folder=os.path.join(exec_dir, current['interface']['view-panes']['template-dir']),
    static_folder=os.path.join(exec_dir, current['interface']['view-panes']['static-dir'])
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['view-panes']['template-dir'],
    # static_folder=settings['interface']['view-panes']['static-dir']
)
#Background
@database_view.route('background_list', methods=['GET', 'POST'])
def background_list():
    return render_template(
        "panes/database_view/components/background/background_list.html",
        background=sorted(dungeonsheets.background.available_backgrounds, key=lambda x: x.get_id())
    )

@database_view.route('background_view', methods=['GET', 'POST'])
def background_view():
    bg_id = request.form.get('id')
    use_bg = None

    for i in dungeonsheets.background.available_backgrounds:
        if i.get_id() == bg_id:
            use_bg = i
            break

    return render_template(
        "panes/database_view/components/background/background_view.html",
        bg=use_bg
    )

# Classes
@database_view.route('class_list', methods=['GET', 'POST'])
def class_list():
    return render_template(
        "panes/database_view/components/class/class_list.html",
        classes=sorted(dungeonsheets.classes.available_classes, key=lambda x: x.get_id())
    )

@database_view.route('subclass_list', methods=['GET', 'POST'])
def subclass_list():
    cls_id = request.form.get('class_id')
    base_class = dungeonsheets.classes.get_class(cls_id)
    return render_template(
        "panes/database_view/components/class/subclass_list.html",
        base_class=base_class,
        subclasses=sorted(base_class.subclasses_available, key=lambda x: x.get_id())
    )


@database_view.route('class_view', methods=['GET', 'POST'])
def class_view():
    cls_id = request.form.get('class_id')

    return render_template(
        "panes/database_view/components/class/class_view.html",
        cls=dungeonsheets.classes.get_class(cls_id)
    )

@database_view.route('subclass_view', methods=['GET', 'POST'])
def subclass_view():
    cls_id = request.form.get('class_id')
    subcls_id = request.form.get('subclass_id')

    base_class = dungeonsheets.classes.get_class(cls_id)
    subclass = base_class.get_subclass(subcls_id)
    return render_template(
        "panes/database_view/components/class/subclass_view.html",
        base_class=base_class,
        subclass=subclass
    )

# Races
@database_view.route('race_list', methods=['GET', 'POST'])
def race_list():
    return render_template(
        "panes/database_view/components/race/race_list.html",
        races=sorted(dungeonsheets.race.available_races, key=lambda x: x.get_id())
    )

@database_view.route('race_view', methods=['GET', 'POST'])
def race_view():
    race_id = request.form.get('id')
    use_race = None

    for i in dungeonsheets.race.available_races:
        if i.get_id() == race_id:
            use_race = i
            break

    return render_template(
        "panes/database_view/components/race/race_view.html",
        race=use_race
    )

@database_view.route('table_result', methods=['GET', 'POST'])
def table_result():
    table_name = request.form.get('table_name')
    table: Table = db.Base.metadata.tables[table_name]

    result = db.db_engine.execute(f"SELECT * FROM {table_name}")

    return render_template(
        "panes/database_view/components/db_table/table_result.html",
        table=table,
        result=result
    )