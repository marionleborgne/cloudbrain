var gulp = require('gulp');
var browserSync = require('browser-sync').create();
var reload = browserSync.reload;

var pkg = require('./package.json');

/** Run local server to host ui folder
*/
gulp.task('serve:ui', function() {
  browserSync.init({
    port:5000,
    server: {
      baseDir: './'
    }
  });
  var watchPaths = ['./**/*.html', './**/*.js', './**/*.css'];
  var ignoreWatching = ['./bower_components/**', './node_modules/**'];
  var ignorePaths = ignoreWatching.map(function (ignorePath){
  	return '!' + ignorePath;
  });
  watchPaths = watchPaths.concat(ignorePaths);
  //Watch and Livereload html, js, and css files in all folders
  gulp.watch(watchPaths, reload);
});

gulp.task('default', ['serve:ui']);
