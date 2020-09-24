
console.log("loading Python_Wrapper");

window.std_handler__main_stdout = null;
window.std_handler__main_stdout_as_html = null;
window.std_handler__main_stdout_updated = null;

let py = null;
// let py_exec = null;

window.addEventListener('pywebviewready', function() {
    
    py = {
        campaign: {
            character: {
                apply_character_text: pywebview.api.campaign.character.apply_character_text,
                get_character_text: pywebview.api.campaign.character.get_character_text,
                get_loaded_characters: pywebview.api.campaign.character.get_loaded_characters,
                load_character: pywebview.api.campaign.character.load_character,
                reload_character: pywebview.api.campaign.character.reload_character,
                save_character: pywebview.api.campaign.character.save_character,
                unload_character: pywebview.api.campaign.character.unload_character
            }
        },
        close_debug: pywebview.api.close_debug,
        exec: pywebview.api.exec,
        files: {
            exists: pywebview.api.files.exists,
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
