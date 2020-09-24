const path = require('path');

module.exports = {
    entry: {
        pdfjs: 'pdfjs-dist'
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, './static/pack'),
    },
};