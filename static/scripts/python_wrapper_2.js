
console.log("loading Python_Wrapper");

window.std_handler__main_stdout = null;
window.std_handler__main_stdout_as_html = null;

let py = null;
// let py_exec = null;

window.addEventListener('pywebviewready', function() {
    
    py = {
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