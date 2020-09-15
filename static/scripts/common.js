'use strict';

function copy_json(json_in) {
    return JSON.parse(JSON.stringify(json_in));
}

function showdown_convert(elem, header_param = 2) {
    let converter = new showdown.Converter();
    converter.setOption('headerLevelStart', header_param);

    console.log(elem.innerHTML);

    elem.innerHTML = converter.makeHtml(elem.innerHTML.trim());
}