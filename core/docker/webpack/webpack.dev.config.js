const path = require('path');

// https://github.com/webpack/webpack.js.org/issues/4106
class WatchRunPlugin {
  apply(compiler) {
      compiler.hooks.watchRun.tap('WatchRun', (comp) => {
          if (comp.modifiedFiles) {
              const changedFiles = Array.from(comp.modifiedFiles, (file) => `\n  ${file}`).join('');
              console.log('===============================');
              console.log('FILES CHANGED:', changedFiles);
              console.log('===============================');
          }
      });
  }
}

module.exports = {
  plugins: [
    new WatchRunPlugin()
  ],
  mode: "development", // If you remove this an infinite loop will occur from the watcher due to how the sass works!
                      // Make sure you disable the watcher too!
                      // https://github.com/webpack/webpack/issues/6901
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
