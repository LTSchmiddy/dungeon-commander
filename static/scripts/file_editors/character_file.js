"use strict";

/** @type {PyNamespace} */
let char_ns = null;

window.addEventListener('pywebviewready', (e)=>{
    char_ns = new PyNamespace('char_editor', async (obj)=>{
        if (obj.created_new) {
            await obj.run(`               
                editors_count = {}
                
                def count_total(path):
                    global editors_count
                    
                    #for uid in editors_count.keys():
                    #    if uid not in viewport.windows.keys():
                    #    del editors_count[uid]
                    
                    retVal = 0
                    for key, value in editors_count.items():
                        retVal += len(list(filter(lambda x: x == path, value)))
                    return retVal
                    
                def add_window(uid):
                    global editors_count
                    editors_count[uid] = []
                
                def add_path(uid, path):
                    global editors_count
                    editors_count[uid].append(path)
                
                def remove_path(uid, path):
                    global editors_count
                    editors_count[uid].remove(path)
                    
                def remove_window(uid):
                    global editors_count
                    del editors_count[uid]
            `);
        }

        await obj.call(`add_window`, [], {uid: window.uid});
    });

    // $(window).bind('beforeunload', ()=>{
    $(window).bind('unload', async ()=>{
        char_ns.cef_call(`remove_window`, [], {uid: window.uid});
    });
});



class CharacterEditorData extends EditorDataBase{

    constructor(elem, name, path, container_selector = ".editor-content", editor_options = {}) {
        super(elem, name, path, container_selector, editor_options);
        this.ref_id = path.replace("?char", "");
        this.editor_type = 'character';
        this.json_editor = null;
        this.original_json = ""
        this.ace_editor = null;
        // this.ace_editor_session = null;
        this.original_code = "";

        this.regen_on_switch_tabs = true;

        this.mode = 'display';

        // DOM Objects:
        // this.editor_tab = this.get_editor_tab();
        // this.editor_view = this.get_editor_view();
        // this.editor_container = this.get_editor_container();
        this.display_view = this.get_display_view();
        this.json_view = this.get_json_view();
        this.ace_view = this.get_ace_view();
        this.ace_editor_container = this.get_ace_editor_container();
        this.ace_status_container = this.get_ace_status_container();

        this.is_changed = false;
        this._should_check_is_changed = false;
        this.edit_loop = null;
        // this.edit_loop = null;

        // char display DOM Object:

        // Async Loading:
        this._async_construction(editor_options);
    }

    get_json_editor_options() {
        let self = this;

        return {
            modes: ['tree', 'view', 'form', 'preview'],

            onChangeJSON: (current_json)=>{
                this.on_json_editor_change(current_json);
            }

        }
    }

    on_switch_to() {
        super.on_switch_to();
        // console.log("Hello");

    }

    async _async_construction(editor_options) {
        this.update_char_display();
        this.load_ace_editor();
        this.get_ace_view().hide();


        this.json_editor = new JSONEditor(this.get_json_view().get()[0], this.get_json_editor_options());

        await this.load_char_json();
        this.get_json_view().hide();
        this.set_original_json();

        await char_ns.call(`add_path`, [], {uid: window.uid, path: this.path});

        // this.update_edited_from_file();

        this.edit_loop = async(me, editor, delay= 2000)=>{
            if (editor._should_check_is_changed) {
                await editor.update_edited_from_file();
                editor._should_check_is_changed = false;
            }

            // console.log("updated");
            if (editor.edit_loop === null) {
                return;
            }
            setTimeout(()=>{me(me, editor, delay)}, delay);
        }
        // edit_loop.bind(edit_loop);
        this.edit_loop(this.edit_loop, this);

    }


    set_original_json() {
        this.original_json = copy_json(this.get_json());
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


    get_json_view() {
        return $(`div[data-char-json-id="${this.path}"]`);
    }

    // Other:
    async load_display_view() {
        await this.get_display_view().load(`/panes/campaign_view/get_character/${this.ref_id}`);
        this.get_display_view().trigger('load');
    }

    load_ace_editor() {
        console.log(this.ace_editor_container.attr('id'));
        this.ace_editor = ace.edit(this.ace_editor_container.attr('id'));
        this.ace_editor.setTheme("ace/theme/cobalt");
        this.ace_editor.session.setMode("ace/mode/python");
        this.ace_editor.on('change', this.on_ace_editor_change.bind(this));
        this.load_ace_char_text();
    }

    async load_char_json() {
        let file_json = await py.campaign.character.get_character_json(this.ref_id);
        if (JSON.stringify(file_json) !== JSON.stringify(this.json_editor.get())) {
            this.json_editor.set(file_json);
        }

    }

    async load_ace_char_text() {
        this.ace_editor.setValue(await py.campaign.character.get_character_text(this.ref_id), 1);
    }

    async apply_ace_char_text(verbose = true) {
        let result = await py.campaign.character.apply_character_text(this.ref_id, this.ace_editor.getValue(), verbose);
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
    }

    async apply_char_json(verbose = true) {
        let result = await py.campaign.character.apply_character_json(this.ref_id, this.json_editor.get(), verbose);
        // if (result === null) {
        //     this.ace_status_container.html(`No errors.`);
        //     this.ace_status_container.addClass('valid');
        //     this.ace_status_container.removeClass('invalid');
        //     // this.update_char_display();
        // } else {
        //     console.log(result.args);
        //     this.ace_status_container.html(`Error : ${result.args.toString().replace(',', ',   ')}`); //"${result.text}"
        //     this.ace_status_container.addClass('invalid');
        //     this.ace_status_container.removeClass('valid');
        // }
    }


    update_char_display() {
        this.load_display_view();
    }

    apply_char() {
        if (this.mode === 'display') {
        }
        else if (this.mode === 'ace') {
            this.apply_ace_char_text();
        }
        else if (this.mode === 'json') {
            this.apply_char_json();
        }
    }

    change_editor_mode(mode) {
        if (this.regen_on_switch_tabs) {
            this.apply_char();
        }

        this.set_editor_mode(mode);
        this.update_edited_from_file();
    }

    set_editor_mode(mode) {

        this.mode = mode;

        if (mode === 'display') {
            this.ace_view.hide();
            this.display_view.show();
            if (this.regen_on_switch_tabs) {
                this.load_display_view();
            }
            window.cqApi.reevaluate(1);
        }
        else if (mode === 'ace') {
            this.display_view.hide();
            this.json_view.hide();
            this.ace_view.show();
            if (this.regen_on_switch_tabs) {
                this.load_ace_char_text();
            }

        }
        else if (mode === 'json') {
            this.display_view.hide();
            this.json_view.show();
            this.ace_view.hide();
            if (this.regen_on_switch_tabs) {
                this.load_char_json();
            }
        }
    }

    get_json() {
        return this.json_editor.get();
    }

    set_json(json_obj) {
        this.json_editor.set(json_obj);
    }

    async refresh() {
        // if (this.mode === 'ace') {
        //     await this.apply_ace_char_text();
        // }
        // else if (this.mode === 'json') {
        //     await this.apply_char_json();
        // }
        this.load_char_json();
        this.load_ace_char_text();
        this.load_display_view();
    }

    async save_file() {
        console.log("saving");
        await py.campaign.character.save_character(this.ref_id);
        this.update_edited_display(false);
        // await this.on_general_change();
        await super.save_file();
    }

    async revert_file() {
        await super.revert_file();
        await py.campaign.character.reload_character(this.ref_id);
        this.update_edited_display(false);
        this.refresh();
    }

    async update_edited_from_file() {
        if (await py.campaign.character.char_id_exists(this.ref_id)){
            this.update_edited_display(await py.campaign.character.is_character_edited(this.ref_id))
        }
    }

    update_edited_display(is_changed = null) {
        if (is_changed !== null) {
            this.is_changed = is_changed;
        }

        let editor_tab = this.get_editor_tab();
        if (editor_tab === null){
            return;
        }
        let editor_tab_dom = editor_tab.get()[0];
        editor_tab_dom.children[1].children[1].innerText = this.is_changed ? " *" : "";

        py.campaign.character.get_char_attr(this.ref_id, 'name').then((name)=>{
            editor_tab_dom.children[1].children[0].innerText = name;
        });
    }

    async on_display_change() {
        await this.on_general_change();
    }

    async on_ace_editor_change(e) {
        if ((await py.settings.get_current_settings())['game']['editors']['character']['auto_update_text_default']){
            await this.apply_ace_char_text(false);
        }
        await this.on_general_change();
    }
    async on_json_editor_change (current_json) {
        if ((await py.settings.get_current_settings())['game']['editors']['character']['auto_update_json_default']){
            await this.apply_char_json(false);
        }
        await this.on_general_change();
    }

    async on_general_change() { //.get()[0]
        // await py.campaign.character.is_character_edited(this.path) ? "*" : "";
        if (!this.is_changed) {
            this.update_edited_from_file();
        }

        this._should_check_is_changed = true;
    }

    async on_close() {
        this.edit_loop = null;
        super.on_close();
        // if (await py.exec(`return not game.current.is_dm`)) {
        //     await py.campaign.character.unload_character(this.ref_id);
        // }

        await char_ns.call(`remove_path`, [], {uid: window.uid, path: this.path});

        campaign_view_update_loaded_characters();
    }

}




// async function _extracted_file_load_character_editor(name, path) {
//     if (!mod_editor_opened_tabs.hasOwnProperty(path)) {
//         console.log(`'${path}' not opened...`);
//         return null;
//     }
//
//
//     $.post("/panes/campaign_view/editors/character_editor", {name: name, id: path}, async (data, status) => {
//         await extracted_file_show_editor("");
//         let container = elem_from_src(data);
//         extracted_file_editor_area.get()[0].appendChild(container);
//
//         let editor_data = mod_editor_opened_tabs[path];
//         editor_data.data_obj = new CharacterEditorData(container, name, path);
//
//         extracted_file_show_editor(path);
//
//     });
//
//
// }