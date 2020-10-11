class EditorDataBase {

    constructor(elem, name, path, container_selector = ".editor-content", editor_options = {}) {
        this.elem = elem;
        this.name = name;
        this.path = path;
        this.container_selector = container_selector;

        /** @type {$} */
        this.editor_view = this.get_editor_view();

        /** @type {Element} */
        this.editor_container = this.get_editor_container();
    }

     // DOM Object Getters:
    get_editor_view() {
        return extracted_file_get_editor(this.path);

    }

    get_editor_tab() {
        return extracted_file_get_tab(this.path);
    }

    get_editor_container() {
        return this.get_editor_view().children(this.container_selector).get()[0];
    }

    switch_to() {
        extracted_file_show_editor(this.path);
    }

    async save_file() {
        campaign_view_reload_dir();
    }

    async revert_file() {}

    async load_state() {}

    async dump_state() {}

    on_switch_to() {}

    on_switch_from() {}

    on_close() {
    }

}

async function _extracted_file_load_new_editor(name, path, ui_path, data_class) {
    if (!mod_editor_opened_tabs.hasOwnProperty(path)) {
        console.log(`'${path}' not opened...`);
        return null;
    }
        // console.log(path);

    $.post(ui_path, {name: name, path: path}, async (data, status) => {
        await extracted_file_show_editor("");
        let container = elem_from_src(data);

        extracted_file_editor_area.get()[0].appendChild(container);

        let editor_data = mod_editor_opened_tabs[path];
        editor_data.data_obj = new data_class(container, name, path);
        container.editor_data = editor_data.data_obj;

        extracted_file_show_editor(path);

    });


}