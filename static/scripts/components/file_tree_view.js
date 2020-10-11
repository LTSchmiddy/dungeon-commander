"use strict";

const _file_tree_view_instances = {};

class FileTreeView {
    /**
     *
     * @param {string} file_view_id
     * @param {string} path
     * @param {Element} container
     */
    constructor(file_view_id, path, container) {

        /** @type {string} */ this.file_view_id = file_view_id;
        _file_tree_view_instances[this.file_view_id] = this;

        /** @type {string} */ this.path = path;
        /** @type {Element} */ this.container = container;

        /** @type {Element} */ this.current_dragee = null;

        this._async_constructor();
    }

    async _async_constructor() {
        /** @type {ChildNode} */ let dom_tree = elem_from_src(await load_html('/panes/file_tree_dir_listing', {path: this.path}));
        await this.parse_DOM_nodes(dom_tree);
        this.container.innerHTML = "";
        this.container.appendChild(dom_tree);
    }

    async parse_DOM_nodes(/** @type {ChildNode} */ node) {
        _.forEach(node.children, (/** @type {ChildNode} */ c_node, index) => {
            // console.log(node);
            c_node.file_view = this;
            c_node.path_type = c_node.getAttribute('data-file-tree-type');
            c_node.path = c_node.getAttribute('data-file-tree-path');

            if (c_node.getAttribute('data-file-tree-type') === 'dir') {
                this.construct_dir_node(c_node);
            } else if (c_node.getAttribute('data-file-tree-type') === 'file') {
                // console.log('file');
                this.construct_file_node(c_node);
            }
        });
    }

    construct_dir_node(/** @type {ChildNode} */ node) {
        let jnode = $(node);

        /*jnode.on('dragstart', _file_view_file_ondragstart);
        jnode.on('dragend', _file_view_file_ondragend);

        jnode.on('dragover',_file_view_dir_ondragover);

        jnode.on('drop',_file_view_dir_ondrop);*/
    }

    construct_file_node(/** @type {ChildNode} */ node) {
        let jnode = $(node);
        // node.addEventListener('drag', (e)=>{ //});


/*        jnode.on('dragstart', _file_view_file_ondragstart);
        jnode.on('dragend', _file_view_file_ondragend);*/
    }

}

/**
 * @param {jQuery.Event} e
 */
function _file_view_file_ondragstart(e) {
    // console.log(e.target.file_view);
    e.target.file_view.current_dragee = e.target;

    e.originalEvent.dataTransfer.setData('src_file_view_id', e.target.file_view.file_view_id);

}

/**
 * @param {jQuery.Event} e
 */
function _file_view_file_ondragend(e) {
    e.target.file_view.current_dragee = null;
}
/**
 * @param {jQuery.Event} e
 */
function _file_view_dir_ondragover(e) {
    e.preventDefault();
}

/**
 * @param {jQuery.Event} e
 */
function _file_view_dir_ondrop(e) {
    // console.log(e);
    /** @type {Element} */
    let dragee = _file_tree_view_instances[e.originalEvent.dataTransfer.getData("src_file_view_id")].current_dragee;
    console.log(dragee);
}

