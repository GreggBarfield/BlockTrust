const path = require('path');

module.exports = {
  entry: {
    manager: path.resolve(__dirname, './core/static/js/widgets/manager.mjs'),
    // https://github.com/webpack-contrib/extract-text-webpack-plugin/issues/518
    ignoreme1: path.resolve(__dirname, './core/static/css/dashboard/dashboard_main.scss'),
  },
  devtool: 'source-map', // DISABLE IN PRODUCTION! SLOW
  output: {
    filename: 'build_[name].min.mjs',
    path: path.resolve(__dirname, './core/static/build'),
  },
  watch: true,
  watchOptions: {
    poll: 500
  },
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,//need to add extract-loader, post-css, 
        use: [
          {
            loader: "file-loader",
            options: {
              name: 'build_[name].min.css',
            },
          },
          "sass-loader",
        ],
      },
    ],
  },
};
