import webpack from 'webpack';
import path from 'path';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import CopyWebpackPlugin from 'copy-webpack-plugin';
const autoprefixer = require('autoprefixer');
export default {
  debug: true,
  devtool: 'cheap-module-eval-source-map',
  noInfo: false,
  entry: [
    'babel-polyfill',
    'eventsource-polyfill', // necessary for hot reloading with IE
    'webpack-hot-middleware/client?reload=true', //note that it reloads the page if hot module reloading fails.
    'ie-find',
    'react',
    'react-dom',
    './src/index'
  ],
  target: 'web',
  output: {
    path: __dirname + '/dist', // Note: Physical files are only output by the production build task `npm run build`.
    publicPath: '/',
    filename: 'ChitChat.js?[hash]'
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  devServer: {
    contentBase: './src'
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new HtmlWebpackPlugin({
      template: 'src/index.html',
      filename: 'index.html',
      inject: true
    }),
    new CopyWebpackPlugin([
      { from: 'src/static/styles/css/loading.min.css', to: 'static/styles/loading.min.css' },
      { from: 'src/static/img/logo.png', to: 'static/img/ChitChat-logo.png' }
    ])
  ],
  module: {
    loaders: [
      { test: /\.js(x?)$/, include: path.join(__dirname, 'src'), loaders: ['babel'] },
      { test: /(\.css)$/, loaders: ["style-loader", "css-loader?-minimize", 'postcss-loader'] },
      { test: /\.scss$/, loaders: ["style-loader", "css-loader?-minimize", 'postcss-loader', "sass-loader"] },
      { test: /\.(jpe?g|png|gif|svg|ico)$/i, loader: 'file-loader?name=static/img/[name].[ext]' },
      { test: /\.(otf|eot|svg|ttf|woff2?)(\?v=\d+\.\d+\.\d+)?$/, loader: 'file-loader?name=static/font/[name].[ext]' }
    ]
  },
  postcss: [autoprefixer({ browsers: ['> 0%'] })]
};
