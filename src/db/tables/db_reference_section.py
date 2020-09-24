from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db


class DB_ReferenceSection(db.Base):
    __tablename__ = 'reference_section'
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown Section")
    parent = Column(String, default="Unknown Parent Section")
    index = Column(Integer, default=1)
    content = Column(String, default="CONTENT")

    _original_json = Column(JSON, default={})

    manual_structure = {}

    def __str__(self):
        return self.id

    def __repr__(self):
        return '\"{:s}\"'.format(str(self))

    @property
    def content_html(self):
        out_content = self.content.replace("||", "||\n||").replace("|", "||")
        return markdown2.markdown(out_content, extras=['wiki-tables'])

    @staticmethod
    def add_json(json_data: dict):
        this_section=db.Session.query(DB_ReferenceSection).filter(DB_ReferenceSection.id == json_data["id"]).first()
        is_new = False

        if this_section is None:
            this_section = DB_ReferenceSection()
            is_new = True

        # print(json_data)

        this_section.id = json_data["id"]
        this_section.name = json_data["name"]
        this_section.parent = json_data["parent"]
        this_section.content = json_data["desc"]

        this_section._original_json = json_data

        if is_new:
            db.Session.add(this_section)

    @classmethod
    def generate_reference_structure(cls):
        for s in db.Session.query(DB_ReferenceSection).all():
            my_json = s._original_json.copy()
            my_json['desc'] = ""

            # Assume Top Level
            if s.parent not in cls.manual_structure:
                cls.manual_structure[s.parent] = {}

            index_val = len(cls.manual_structure[s.parent]) + 1
            if s.parent == s.name:
                index_val = 0

            cls.manual_structure[s.parent][f"{index_val}. {s.name}"] = my_json
            s.index = index_val

    @classmethod
    def get_sorted_reference(cls):
        return db.Session.query(DB_ReferenceSection).order_by(DB_ReferenceSection.parent, DB_ReferenceSection.index).all()



