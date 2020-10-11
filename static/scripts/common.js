'use strict';

// JQuery get text preserve whitespace:
(function($){
   $.fn.innerText = function(msg) {
         if (msg) {
            if (document.body.innerText) {
               for (let i in this) {
                  this[i].innerText = msg;
               }
            } else {
               for (let i in this) {
                  this[i].innerHTML.replace(/&amp;lt;br&amp;gt;/gi,"n").replace(/(&amp;lt;([^&amp;gt;]+)&amp;gt;)/gi, "");
               }
            }
            return this;
         } else {
            if (document.body.innerText) {
               return this[0].innerText;
            } else {
               return this[0].innerHTML.replace(/&amp;lt;br&amp;gt;/gi,"n").replace(/(&amp;lt;([^&amp;gt;]+)&amp;gt;)/gi, "");
            }
         }
   };
})(jQuery);




function copy_json(json_in) {
    return JSON.parse(JSON.stringify(json_in));
}

function showdown_convert(elem, header_param = 2) {
    let converter = new showdown.Converter();
    converter.setOption('headerLevelStart', header_param);

    console.log(elem.innerHTML);

    elem.innerHTML = converter.makeHtml(elem.innerHTML.trim());
}

/**
 *
 * @param {string} code
 * @returns {ChildNode}
 */
function elem_from_src(code) {
    let wrapper = document.createElement('div');
    wrapper.innerHTML = code;
    return wrapper.firstChild;
}

/**
 *
 * @param {string} code
 * @returns {NodeListOf<ChildNode>}
 */
function elems_from_src(code) {
    let wrapper = document.createElement('div');
    wrapper.innerHTML = code;
    return wrapper.childNodes;
}

/**
 *
 * @param {string} tag
 * @param {string} code
 * @returns {Element}
 */
function elem_from_tag(tag, code="") {
    let wrapper = document.createElement(tag);
    wrapper.innerHTML = code;
    return wrapper;
}


/**
 *
 * @param {string} addr
 * @param {object} params
 * @returns {Promise<string>}
 */
async function load_html(addr, params={}) {
    return (await $.post(addr, params)).trim();
}

// function char_keep_field_updated(field, trigger_fields, callback) {
//     for (let i = 0; i < trigger_fields.length; i++) {
//         let my_field = trigger_fields[i];
//
//         $(my_field).on('change', callback);
//     }
// }

function allowDrop(ev) {
  ev.preventDefault();
}

/**
 *
 * @param {string} name
 * @param {string} path
 */
function open_file_handler(name, path) {
    if (path.endsWith(".dc_char")) {
        py.campaign.character.load_character(path).then(async (new_char_id)=>{

            campaign_view_update_loaded_characters();
            if (await py.exec(`return not game.current.is_dm`)) {
                extracted_file_load(await py.campaign.character.get_char_attr(new_char_id, 'name'), new_char_id + "?char");
            }
        });

    } else {
        extracted_file_load(name, path);
    }
}

exposed_functions.push(open_file_handler);

/**
 *
 * @param {object} obj
 * @param {string} prefix
 */
function context_menu_nesting(obj, prefix="") {
    let retVal = {};
    // console.log(_.keysIn(obj));
    _.forEach(_.keysIn(obj), (key, index)=>{
        let val = obj[key];
        let new_key = prefix + key;

        if (val.hasOwnProperty('items')){
            val['items'] = context_menu_nesting(val['items'], key + "/");
        }
        retVal[new_key] = val;
    });


    return retVal;
}