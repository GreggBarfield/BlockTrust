const path = require('path');

const { exec } = require('child_process');
exec('ls', (err, stdout, stderr) => {
  if (err) {
    //some err occurred
    console.error(err)
  } else {
   // the *entire* stdout and stderr (buffered)
   console.log(`stdout: ${stdout}`);
   console.log(`stderr: ${stderr}`);
  }
});

module.exports = {
  mode: "production", // If you remove this an infinite loop will occur from the watcher due to how the sass works!
                      // Make sure you disable the watcher too!
                      // https://github.com/webpack/webpack/issues/6901
  entry: {
    manager: path.resolve(__dirname, './core/static/js/widgets/manager.mjs'),
    outside_interactive: path.resolve(__dirname, './core/static/js/outside/interactive.mjs'),
    // https://github.com/webpack-contrib/extract-text-webpack-plugin/issues/518
    standalone_assets: path.resolve(__dirname, './core/static/css/dashboard/dashboard_main.scss'),
  },
  devtool: 'source-map', // DISABLE IN PRODUCTION! SLOW
  output: {
    filename: 'build_[name].min.mjs',
    path: path.resolve(__dirname, './core/static/build'),
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
