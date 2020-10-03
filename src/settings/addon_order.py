import os
import json
from typing import List, Dict

import util


def scan_addon_directory(path: str, addon_list: list):
    found_files = []
    found_dirs = []

    force_default_load_order = False

    # Check for default_load_order:
    module_info_path = os.path.join(path, "module_info.json")
    if os.path.isfile(module_info_path):
        module_info = json.load(open(module_info_path, 'r'))

        if 'force' in module_info and module_info['force'] == True:
            force_default_load_order = module_info['force']
            print(force_default_load_order)
            addon_list.clear()
            print(f"Module '{path}' requires use of default load order.")

        if len(addon_list) <= 0:
            if "order" in module_info:
                print(f"Default load order detected for {path}. Loading now...")
                addon_list.extend(module_info["order"])



    for i in os.listdir(path):
        # Ignoring compiled python code files (`__pycache__` directories).
        if i == "__pycache__":
            continue

        fullpath = os.path.join(path, i)

        # Adding new files/folders:
        # Handle code files:
        if os.path.isfile(fullpath):
            if i.endswith(".py"):
                found_files.append(i)
                print(f"Module file found: {fullpath}")
                if i not in addon_list:
                    addon_list.append(i)

        # Handling folders:
        elif os.path.isdir(fullpath):
            print(f"Sub-directory found: {fullpath}")
            found_dirs.append(i)

            dir_dict: (dict, None) = util.list_get(
                (
                    lambda x: (isinstance(x, dict))
                    and ("name" in x)
                    and ("contents" in x)
                    and ("force_default_load_order" in x)
                    and (x["name"] == i)
                ),
                addon_list,
            )

            if dir_dict is None:
                dir_dict = {"name": i, "contents": [], "force_default_load_order": force_default_load_order}

                addon_list.append(dir_dict)


            dir_dict["force_default_load_order"] = scan_addon_directory(fullpath, dir_dict["contents"])



    # removing old files:
    to_remove = []
    for i in range(0, len(addon_list)):
        item = addon_list[i]
        if isinstance(item, str) and item not in found_files:
            to_remove.append(i)

        elif isinstance(item, dict) and item['name'] not in found_dirs:
            to_remove.append(i)

    for i in to_remove:
        del addon_list[i]


    return force_default_load_order
    # print()
