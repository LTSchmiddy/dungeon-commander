
class CreatureEditorData extends EditorDataBase {


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
        let file_json = await py.campaign.creature.get_creature_json(this.path);

        this.editor = new JSONEditor(this.get_editor_container(), this.get_editor_options());
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
        await py.campaign.creature.apply_creatures_json(this.path, this.get_json());
        await py.campaign.creature.save_creature(this.path);
        this.set_original_json();
        await super.save_file();
    }

    async revert_file() {
        this.set_json(await py.campaign.creature.get_creature_json(this.path));
        this.set_original_json();
        await super.revert_file();
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