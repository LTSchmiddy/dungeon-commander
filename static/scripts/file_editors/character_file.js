

class CharacterEditorData {
    constructor(elem, name, path, container_selector = ".editor-content", editor_options = {}) {
        this.elem = elem;
        this.name = name;
        this.path = path;
        this.editor_type = 'character';
        this.container_selector = container_selector;
        this.json_editor = null;
        this.original_json = ""
        this.ace_editor = null;
        // this.ace_editor_session = null;
        this.original_code = "";

        this.mode = 'display';

        // DOM Objects:
        this.editor_view = this.get_editor_view();
        this.editor_container = this.get_editor_container();
        this.display_view = this.get_display_view();
        this.ace_view = this.get_ace_view();
        this.ace_editor_container = this.get_ace_editor_container();
        this.ace_status_container = this.get_ace_status_container();

        // Async Loading:
        this._async_construction(editor_options);
    }

    get_editor_options() {
        let self = this;

    }

    async _async_construction(editor_options) {
        this.update_char_display();
        this.load_ace_editor();
        this.get_ace_view().hide();
    }

    // DOM Object Getters:
    get_editor_view() {
        return extracted_file_get_editor(this.path);
    }

    get_editor_container() {
        return this.get_editor_view().children(this.container_selector).get()[0];
    }

    get_display_view() {
        return $(`div[data-char-display-id="${this.path}"]`);
    }

    get_ace_view() {
        return $(`div[data-char-ace-id="${this.path}"]`);
    }

    get_ace_editor_container() {
        return $(`div[data-char-ace-editor-id="${this.path}"]`);
    }

    get_ace_status_container() {
        return $(`div[data-char-ace-status-id="${this.path}"]`);
    }

    // Other:
    load_display_view() {
        this.get_display_view().load(`/panes/campaign_view/get_character/${this.path}`);
    }



    load_ace_editor() {
        console.log(this.ace_editor_container.attr('id'));
        this.ace_editor = ace.edit(this.ace_editor_container.attr('id'));
        this.ace_editor.setTheme("ace/theme/cobalt");
        this.ace_editor.session.setMode("ace/mode/python");
        this.ace_editor.on('change', this.on_editor_change.bind(this));
        this.load_ace_char_text();

    }

    async load_ace_char_text() {
        this.ace_editor.setValue(await py.campaign.character.get_character_text(this.path), 1);
    }

    async apply_ace_char_text() {
        let result = await py.campaign.character.apply_character_text(this.path, this.ace_editor.getValue());
        if (result === null) {
            this.ace_status_container.html(`No errors.`);
            this.ace_status_container.addClass('valid');
            this.ace_status_container.removeClass('invalid');
            // this.update_char_display();
        } else {
            console.log(result.args);
            this.ace_status_container.html(`Error : ${result.args.toString().replace(',', ',   ')}`); //"${result.text}"
            this.ace_status_container.addClass('invalid');
            this.ace_status_container.removeClass('valid');
        }

        // return result;
    }

    switch_to() {
        extracted_file_show_editor(this.path);
    }

    update_char_display() {
        this.load_display_view();
    }

    set_editor_mode(mode) {
        this.mode = mode;

        if (mode === 'display') {
            this.ace_view.hide();
            this.display_view.show();
            this.load_display_view();
            window.cqApi.reevaluate(1);
        }
        else if (mode === 'ace') {
            this.display_view.hide();
            this.ace_view.show();

        }

    }

    async regenerate_code() {
        await this.apply_ace_char_text();
        await this.load_ace_char_text();
    }

    async save_file() {
        console.log("saving")
        py.campaign.character.save_character(this.path);
    }

    async revert_file() {
        py.campaign.character.reload_character(this.path);
    }

    async on_editor_change(e) {
        console.log('applying 1');
        await this.apply_ace_char_text();
    }
}




async function _extracted_file_load_character_editor(name, path) {
    if (!mod_editor_opened_tabs.hasOwnProperty(path)) {
        console.log(`'${path}' not opened...`);
        return null;
    }

    $.post("/panes/campaign_view/editors/character_editor", {name: name, id: path}, async (data, status) => {
        await extracted_file_show_editor("");
        let container = generate_element(data);
        extracted_file_editor_area.get()[0].appendChild(container);

        let editor_data = mod_editor_opened_tabs[path];
        editor_data.data_obj = new CharacterEditorData(container, name, path);

        extracted_file_show_editor(path);

    });


}