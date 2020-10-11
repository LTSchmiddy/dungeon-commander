
console.log("loading Python_Wrapper");

window.wvOPEN_DIALOG = null; // global 
window.wvFOLDER_DIALOG = null; // global 
window.wvSAVE_DIALOG = null; // global 
window.expose_js_function = null; // unique 
window.cef_exec = null; // unique 
window.cef_ns_exec = null; // unique 
window.cef_run = null; // unique 
window.cef_ns_run = null; // unique 
window.uid = null; // unique 
window.cef_console_init = null; // unique 

let py = null;
// let py_exec = null;

window.addEventListener('pywebviewready', function() {
    
    py = {
        campaign: {
            character: {
                apply_character_json: pywebview.api.campaign.character.apply_character_json,
                apply_character_text: pywebview.api.campaign.character.apply_character_text,
                call_char_method: pywebview.api.campaign.character.call_char_method,
                char_id_exists: pywebview.api.campaign.character.char_id_exists,
                get_char_attr: pywebview.api.campaign.character.get_char_attr,
                get_character_json: pywebview.api.campaign.character.get_character_json,
                get_character_text: pywebview.api.campaign.character.get_character_text,
                get_loaded_characters: pywebview.api.campaign.character.get_loaded_characters,
                is_character_edited: pywebview.api.campaign.character.is_character_edited,
                load_character: pywebview.api.campaign.character.load_character,
                new_character: pywebview.api.campaign.character.new_character,
                reload_character: pywebview.api.campaign.character.reload_character,
                save_character: pywebview.api.campaign.character.save_character,
                set_char_attr: pywebview.api.campaign.character.set_char_attr,
                set_char_attr_raw: pywebview.api.campaign.character.set_char_attr_raw,
                unload_character: pywebview.api.campaign.character.unload_character
            },
            creature: {
                apply_creatures_json: pywebview.api.campaign.creature.apply_creatures_json,
                creature_id_exists: pywebview.api.campaign.creature.creature_id_exists,
                get_creature_json: pywebview.api.campaign.creature.get_creature_json,
                get_loaded_creatures: pywebview.api.campaign.creature.get_loaded_creatures,
                load_creature: pywebview.api.campaign.creature.load_creature,
                save_creature: pywebview.api.campaign.creature.save_creature,
                spawn_creature: pywebview.api.campaign.creature.spawn_creature,
                unload_creature: pywebview.api.campaign.creature.unload_creature
            },
            eval_dice: pywebview.api.campaign.eval_dice,
            get_abs_campaign_path: pywebview.api.campaign.get_abs_campaign_path,
            get_campaign_path: pywebview.api.campaign.get_campaign_path
        },
        close_debug: pywebview.api.close_debug,
        code: {
            call: pywebview.api.code.call,
            create_namespace_if_dne: pywebview.api.code.create_namespace_if_dne,
            create_new_namespace: pywebview.api.code.create_new_namespace,
            del_var: pywebview.api.code.del_var,
            delete_namespace: pywebview.api.code.delete_namespace,
            fexec: pywebview.api.code.fexec,
            get_globals: pywebview.api.code.get_globals,
            get_locals: pywebview.api.code.get_locals,
            get_new_namespace_id: pywebview.api.code.get_new_namespace_id,
            get_var: pywebview.api.code.get_var,
            has_var: pywebview.api.code.has_var,
            list_globals: pywebview.api.code.list_globals,
            list_locals: pywebview.api.code.list_locals,
            namespace_exists: pywebview.api.code.namespace_exists,
            reset: pywebview.api.code.reset,
            run: pywebview.api.code.run,
            set_globals: pywebview.api.code.set_globals,
            set_locals: pywebview.api.code.set_locals,
            set_var: pywebview.api.code.set_var
        },
        exec: pywebview.api.exec,
        files: {
            exists: pywebview.api.files.exists,
            file_dialog: pywebview.api.files.file_dialog,
            getcwd: pywebview.api.files.getcwd,
            isdir: pywebview.api.files.isdir,
            isfile: pywebview.api.files.isfile,
            link: pywebview.api.files.link,
            listdir: pywebview.api.files.listdir,
            makedirs: pywebview.api.files.makedirs,
            mkdir: pywebview.api.files.mkdir,
            read_file: pywebview.api.files.read_file,
            read_json_file: pywebview.api.files.read_json_file,
            remove: pywebview.api.files.remove,
            write_file: pywebview.api.files.write_file,
            write_json_file: pywebview.api.files.write_json_file
        },
        main: {
            call: pywebview.api.main.call,
            del_var: pywebview.api.main.del_var,
            fexec: pywebview.api.main.fexec,
            get_globals: pywebview.api.main.get_globals,
            get_locals: pywebview.api.main.get_locals,
            get_var: pywebview.api.main.get_var,
            global_reset: pywebview.api.main.global_reset,
            has_var: pywebview.api.main.has_var,
            list_globals: pywebview.api.main.list_globals,
            list_locals: pywebview.api.main.list_locals,
            reset: pywebview.api.main.reset,
            run: pywebview.api.main.run,
            set_globals: pywebview.api.main.set_globals,
            set_locals: pywebview.api.main.set_locals,
            set_var: pywebview.api.main.set_var
        },
        open_debug: pywebview.api.open_debug,
        print: pywebview.api.print,
        quit: pywebview.api.quit,
        settings: {
            get_current_settings: pywebview.api.settings.get_current_settings,
            set_current_settings: pywebview.api.settings.set_current_settings,
            validate_settings: pywebview.api.settings.validate_settings
        },
        std: {
            get_stdout: pywebview.api.std.get_stdout
        }
    }
    
    console.log("pwv ready");
});
