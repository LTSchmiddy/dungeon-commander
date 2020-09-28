"use strict";

// Jquery Loaded
import $ from 'jquery';
import jQuery from 'jquery';
window.$ = jQuery;

// Load Popper.js
import 'popper.js';

// Import Bootstrap
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

console.log("Bootstrap Version: " + $.fn.tooltip.Constructor.VERSION);

import 'store'
import 'jquery-resizable-columns'
import 'jquery-resizable-columns/dist/jquery.resizableColumns.css'