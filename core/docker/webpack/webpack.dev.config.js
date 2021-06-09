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
    new WatchRunPlugin() // for debugging watcher
  ],
  mode: "development", // If you remove this an infinite loop will occur from the watcher due to how the sass works!
                      // Make sure you disable the watcher too!
                      // https://github.com/webpack/webpack/issues/6901
  entry: {
    manager: path.resolve(__dirname, './core/static/js/widgets/manager.mjs'),
    outside_interactive: path.resolve(__dirname, './core/static/js/outside/interactive.mjs'),
    // https://github.com/webpack-contrib/extract-text-webpack-plugin/issues/518
    standalone_assets: path.resolve(__dirname, './core/static/css/dashboard/dashboard_main.scss'),
    outside_main: path.resolve(__dirname, './core/static/css/outside/outside_main.scss')
  },
  devtool: 'source-map', // DISABLE IN PRODUCTION! SLOW
  output: {
    filename: 'build_[name].min.mjs',
    path: path.resolve(__dirname, './core/static/build'),
  },
  watch: true,
  watchOptions: {
    poll: 500 // necessary due to wsl2
  },
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,//need to add extract-loader, post-css, 
        use: [
          "sass-loader"
        ],
        type: "asset/resource",
        generator: {
          filename: "build_[name].min.css"
        }
      },
    ],
  },
};
