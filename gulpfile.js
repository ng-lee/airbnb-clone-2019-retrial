const gulp = require("gulp");

const css = () => {
  const postCSS = require("gulp-postcss");
  const sass = require("gulp-sass")(require("sass"));
  const minify = require("gulp-csso");
  sass.compiler = require("node-sass");
  return gulp
    .src("assets/scss/styles.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(
      postCSS([
        require("@tailwindcss/postcss7-compat"),
        require("autoprefixer"),
      ])
    )
    .pipe(minify())
    .pipe(gulp.dest("static/css"));
};

exports.default = css;
