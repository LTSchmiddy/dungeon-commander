"use strict";

/** @type {PyNamespace} */
let json_ns = null;

window.addEventListener('pywebviewready', (e)=>{
    json_ns = new PyNamespace('json_editor', (obj)=>{
        if (obj.created_new) {
            obj.run(`
                import json
                
                editor_dumps = {}
            `);
        }
    });
});


class JsonFileEditorData extends EditorDataBase {


    constructor(elem, name, path, container_selector = ".editor-content", editor_options = {}) {
        super(elem, name, path, container_selector, editor_options);

        this.editor_type = 'json';
        this.editor = null;
        this.original_json = "";

        this._async_construction(editor_options);
    }

    get_editor_options() {
        let self = this;

        return {
            modes: ['tree', 'view', 'form', 'preview'],

            onChangeJSON: (current_json)=>{
                this.onChangeJSON(current_json);
            }

        }
    }

    async _async_construction(editor_options) {

        this.editor = new JSONEditor(this.get_editor_container(), this.get_editor_options());

        if ((await this.load_state())) {
            return;
        }
        let file_json = await py.files.read_json_file(this.path);
        this.editor.set(file_json);
        this.set_original_json();
    }


    set_original_json() {
        this.original_json = copy_json(this.get_json());
    }


    get_json() {
        // console.log(this.editor.get());
        return this.editor.get();
    }

    set_json(json_obj) {
        this.editor.set(json_obj);
    }



    async save_file() {
        // await py.files.write_json_file(this.path, JSON.stringify(this.get_json()));
        await py.files.write_json_file(this.path, this.get_json());
        this.set_original_json();
        await super.save_file();
    }

    async revert_file() {
        this.set_json(await py.files.read_json_file(this.path));
        this.set_original_json();
        await super.revert_file();
    }

    async load_state() {
        let file_json = await json_ns.fexec(`
            if path not in editor_dumps:
                return None
            
            retVal = editor_dumps[path]
            del editor_dumps[path]
            return retVal
            
        `, {
            path: this.path
        });
        if (file_json !== null) {
            this.editor.set(file_json);
            this.set_original_json();
            return true;
        } else {
            return false;
        }
    }

    async dump_state() {
        return await json_ns.fexec(`
             editor_dumps[e_path] = e_content  
        `, {
            e_path: this.path,
            e_content: this.get_json(),
        });
    }

    is_json_original() {
        return JSON.stringify(this.get_json()) !== JSON.stringify(this.original_json);
    }

    onChangeJSON (current_json) {
        // console.log(this.is_json_original());

        if (this.is_json_original()) {


        }
    }
}




// async function _extracted_file_load_json_editor(name, path) {
//     if (!mod_editor_opened_tabs.hasOwnProperty(path)) {
//         console.log(`'${path}' not opened...`);
//         return null;
//     }
//
//     $.post("/panes/campaign_view/editors/json_editor", {name: name, path: path}, async (data, status) => {
//         await extracted_file_show_editor("");
//         // extracted_file_editor_area.get()[0].innerHTML += data;
//         let container = elem_from_src(data);
//         extracted_file_editor_area.get()[0].appendChild(container);
//
//         let editor_data = mod_editor_opened_tabs[path];
//         editor_data.data_obj = new JsonFileEditorData(container, name, path);
//
//         extracted_file_show_editor(path);
//
//     });
//
//
// }