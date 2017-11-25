import webpack from 'webpack';
import path from 'path';
import ExtractTextPlugin from 'extract-text-webpack-plugin';
import CopyWebpackPlugin from 'copy-webpack-plugin';
import HtmlWebpackPlugin from 'html-webpack-plugin';
const autoprefixer = require('autoprefixer');

const GLOBALS = {
  'process.env.NODE_ENV': JSON.stringify('production')
};

export default {
  debug: true,
  devtool: 'source-map',
  noInfo: false,
  entry: [
    'babel-polyfill',
    'ie-find',
    'react',
    'react-dom',
    './src/index'
  ],
  target: 'web',
  output: {
    path: __dirname + '/dist', // Note: Physical files are only output by the production build task `npm run build`.
    publicPath: '/',
    filename: 'ChitChat.js?v[hash]'
  },
  devServer: {
    contentBase: './dist'
  },
  resolve: {
    modulesDirectories: [
      'src',
      'node_modules'
    ],
    extensions: ['', '.json', '.js', '.jsx']
  },
  plugins: [
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.DefinePlugin(GLOBALS),
    new ExtractTextPlugin('styles.css'),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: false,
      mangle: true
    }
    ),
    new HtmlWebpackPlugin({
      template: 'src/index.html'
    }),
    new CopyWebpackPlugin([
      { from: 'src/static/styles/css/loading.min.css', to: 'static/styles/loading.min.css' },
      { from: 'src/static/img/logo.png', to: 'static/img/ChitChat-logo.png' }
    ])
  ],
  module: {
    loaders: [
      { test: /\.js(x?)$/, include: path.join(__dirname, 'src'), loaders: ['babel'] },
      { test: /(\.css)$/, loaders: ["style-loader", "css-loader?minimize!", 'postcss-loader'] },
      { test: /\.scss$/, loaders: ["style-loader", "css-loader?minimize!", 'postcss-loader', "sass-loader"] },
      { test: /\.(jpe?g|png|gif|svg|ico)$/i, loader: 'file-loader?name=static/img/[name].[ext]' },
      { test: /\.(otf|eot|svg|ttf|woff2?)(\?v=\d+\.\d+\.\d+)?$/, loader: 'file-loader?name=static/font/[name].[ext]' }
    ]
  },
  postcss: [autoprefixer({ browsers: ['> 0%'] })]
};
