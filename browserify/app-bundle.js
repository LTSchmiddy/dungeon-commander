//include:./node_modules/bootstrap/dist/css/bootstrap.css

window.jQuery = $ = require('jquery');

window.Popper = require('popper.js');
// Bootstrap doesn't have a "main" field / export anything =(
const bootstrap = require('bootstrap/dist/js/bootstrap');

window._ = require('lodash');
window.keymage = require('keymage');
window.Sortable = require('sortablejs');

window.showdown = require('showdown');
window.JSONEditor = require('jsoneditor');
//include:./node_modules/jsoneditor/dist/jsoneditor.css
//include:./node_modules/jsoneditor/dist/img

require('jquery-contextmenu');
//include:./node_modules/jquery-contextmenu/dist/jquery.contextMenu.css
//include:./node_modules/jquery-contextmenu/dist/font

// window.pdfjs = require('pdfjs-dist');
// window.pdfjs = require('pdfjs-dist/');
