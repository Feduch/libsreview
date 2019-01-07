const webpack = require('webpack');
const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

const distPath = path.join(__dirname, '/staticfiles/dist/');
const distStaticPath = path.join(__dirname, '/staticfiles/bundles/');

let webpackConfig = {
    optimization: {
        minimizer: [
            new UglifyJsPlugin({
                cache: true,
                parallel: true,
                sourceMap: true // set to true if you want JS source maps
            }),
            new OptimizeCSSAssetsPlugin({})
        ]
    },
    entry: {
        'main': './vue/main.js',
        'navigator': './vue/navigator.js',
        'collections': './vue/collections.js',
        'publications': './vue/publications.js',
        'publications-detail': './vue/publication-detail.js',
        'books': './vue/books.js',
        'book-detail': './vue/book-detail.js',
        'book-read': './vue/book-read.js',
        'authors': './vue/authors.js',
        'author-detail': './vue/author-detail.js',
        'books-admin': './vue/books-admin.js',
        'ratings': './vue/ratings.js',
        'genre-detail': './vue/genre-detail.js',
        'profile': './vue/profile.js',
        'all-page': './vue/all-page.js',
    },
    output: {
        path: distPath,
        filename: '[name]-[hash].js',
        publicPath: '/static/dist/',
    },
    plugins: [
        new CleanWebpackPlugin(distPath),
        new CleanWebpackPlugin(distStaticPath),
        new MiniCssExtractPlugin({
            filename: "[name].[contenthash].css"
        }),
        new VueLoaderPlugin(),
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify('production')
        })
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                options: {
                    babelrc: false,
                    presets: ['es2015'],
                    plugins: ['transform-object-rest-spread','transform-vue-jsx']
                }
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader"
                ]
            }
        ]
    },
    mode: 'development',
    resolve: {
        alias: {
            vue: 'vue/dist/vue.js'
        }
    }
};

module.exports = webpackConfig;
