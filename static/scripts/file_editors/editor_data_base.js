class EditorDataBase {
    constructor(elem, name, path, container_selector = ".editor-content", editor_options = {}) {
        this.elem = elem;
        this.name = name;
        this.path = path;
        this.container_selector = container_selector;
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

    on_switch_to() {}

    on_switch_from() {}

    on_close() {
    }

}