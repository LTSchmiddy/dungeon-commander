'use strict';

// JQuery get text preserve whitespace:
(function($){
   $.fn.innerText = function(msg) {
         if (msg) {
            if (document.body.innerText) {
               for (var i in this) {
                  this[i].innerText = msg;
               }
            } else {
               for (var i in this) {
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

function generate_element(code) {
    let wrapper = document.createElement('div');
    wrapper.innerHTML = code;
    return wrapper.firstChild;
}

async function load_html(addr, params={}) {
    return await $.post(addr, params);
}

// function char_keep_field_updated(field, trigger_fields, callback) {
//     for (let i = 0; i < trigger_fields.length; i++) {
//         let my_field = trigger_fields[i];
//
//         $(my_field).on('change', callback);
//     }
// }