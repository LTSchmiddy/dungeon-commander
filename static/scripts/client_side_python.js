"use strict";
let _py_init_code_list = [];
let _py_init_finished = false;
/**
 *
 * @param {string} p_code
 * @param {string} p_return
 * @param {object} temp_locals
 */
function on_start_py(p_code, p_return="", temp_locals=null) {
    if (_py_init_finished) {
        py.main.run(p_code, p_return, temp_locals);
    } else {
        _py_init_code_list.push({c: p_code, r: p_return, t: temp_locals});
    }
}

window.addEventListener('pywebviewready', async ()=>{
    // await py.main.global_reset();
    for (let i = 0; i < _py_init_code_list.length; i++) {
        let next_code = _py_init_code_list[i];
        await py.main.run(next_code.c, next_code.r, next_code.t);
        // console.log(next_code);
        // await py.main.run();
    }
    _py_init_finished = true;
});

class PyNamespace {
    constructor(name, callback=null, recreate=false, add_main = true, global_level = true) {
        this.name = name;
        this.created_new = true;

        /** @type {Promise} */let init_promise = null;
        if (recreate) {
            init_promise = py.code.create_new_namespace(name, add_main, global_level);
        }
        else {
            init_promise = py.code.create_namespace_if_dne(name, add_main, global_level);
        }
        
        init_promise.then(function(was_old){this.created_new = !was_old; if (callback !== null) {callback(this);}}.bind(this));
    }
    
    async call(...args) {
        return await py.code.call(this.name, ...args);
    }

    cef_call (...args) {
        cef_ns_call(this.name, ...args);
    }

    async create_namespace_if_dne(...args) {
        return await py.code.create_namespace_if_dne(this.name, ...args);
    }
    async create_new_namespace(...args) {
        return await py.code.create_new_namespace(this.name, ...args);
    }
    async del_var(...args) {
        return await py.code.del_var(this.name, ...args);
    }
    async delete_namespace(...args) {
        return await py.code.delete_namespace(this.name, ...args);
    }
    async fexec(...args) {
        return await py.code.fexec(this.name, ...args);
    }

    cef_fexec (...args) {
        cef_ns_exec(this.name, ...args);
    }

    async get_globals(...args) {
        return await py.code.get_globals(this.name, ...args);
    }
    async get_locals(...args) {
        return await py.code.get_locals(this.name, ...args);
    }
    async get_new_namespace_id(...args) {
        return await py.code.get_new_namespace_id(this.name, ...args);
    }
    async get_var(...args) {
        return await py.code.get_var(this.name, ...args);
    }
    async has_var(...args) {
        return await py.code.has_var(this.name, ...args);
    }
    async list_globals() {
        return await py.code.list_globals(this.name);
    }
    async list_locals(...args) {
        return await py.code.list_locals(this.name);
    }
    async namespace_exists(...args) {
        return await py.code.namespace_exists(this.name, ...args);
    }
    async reset(...args) {
        return await py.code.reset(this.name, ...args);
    }
    async run(...args) {
        return await py.code.run(this.name, ...args);
    }

    cef_run (...args) {
        cef_ns_run(this.name, ...args);
    }

    async set_globals(...args) {
        return await py.code.set_globals(this.name, ...args);
    }
    async set_locals(...args) {
        return await py.code.set_locals(this.name, ...args);
    }
    async set_var(...args) {
        return await py.code.set_var(this.name, ...args);
    }
}