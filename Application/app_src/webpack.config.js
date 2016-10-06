var path = require("path");
var webpack = require("webpack");

var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var rootAssetPath = "./";
var fileLoader = "file?context=" + rootAssetPath + "&name=[path][name].[hash].[ext]";

var plugins = [
    new ManifestRevisionPlugin(path.join(rootAssetPath, "manifest.json"), {
      rootAssetPath: rootAssetPath,
      ignorePaths: ["node_modules", "webpack.config.js", "manifest.json", "package.json", ".babelrc"],
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
];

var entry = {
  "app_js": ["babel-polyfill", "./lib/app.js"],
  "app_style": ["./styles/styles.scss"],
};

var sassToCssLoader = ["css?sourceMap", "resolve-url", "sass?sourceMap"];
var cssToFinalLoader = ["style"];

if(process.env.NODE_ENV === 'production'){
  plugins = plugins.concat([
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.optimize.UglifyJsPlugin(),
  ]);
  cssToFinalLoader = ["file?context=" + rootAssetPath + "&name=[path][name].css", "extract"];
}else{
}

module.exports = {
  entry: entry ,
  output: {
    path: "../static",
    publicPath:"/static/",
    filename: "[name].[hash].js",
    chunkFilename: "[id].[chunkhash].js"
  },
  resolve: {
    extensions: ["", ".vue", ".js", ".css"]
  },
  devtool: "eval-source-map",
  module: {
    loaders: [
      //Sass
      {
        test: /\.s(c|a)ss$/,
        loaders: cssToFinalLoader.concat(sassToCssLoader),
      },
      //JS (ES6)
      {
        test: /\.js$/,
        loaders: ["babel"],
        exclude: /node_modules/
      },
      //Fonts
      {
        test : /\.(ttf|svg|eot|woff|woff2)$/,
        loaders: [fileLoader]
      },
      //Vue Components
      {
        test: /\.vue$/,
        loaders: ["vue"]
      }
    ]
  },
  vue: {
    loaders: {
      sass: "vue-style!" + sassToCssLoader.join("!"),
    }
  },
  plugins:plugins,
};
