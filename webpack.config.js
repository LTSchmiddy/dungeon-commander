const webpack = require('webpack');
const path = require('path');

module.exports = {
    entry: {
        pdfjs: 'pdfjs-dist',
        keymage: './webpack/dep_loaders/load_keymage.js'
        // bootstrap_base: './webpack/dep_loaders/bootstrap_base.js',
    },
    plugins: [
        new webpack.ProvidePlugin({
                $: "jquery",
                jQuery: "jquery",

        }),
        new webpack.ProvidePlugin({
                keymage: "keymage",
                "window.keymage": "keymage"
        })
    ],
    module: {
        rules: [
            {
                test: /\.s[ac]ss$/i,
                    use: [
                    // Creates `style` nodes from JS strings
                    'style-loader',
                    // Translates CSS into CommonJS
                    'css-loader',
                    // Compiles Sass to CSS
                    'sass-loader',
                ],
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ],
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, './static/pack'),
    },
};