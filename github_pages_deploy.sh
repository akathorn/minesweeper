cd web-app
ng build --configuration production
rm -r ../../akathorn.github.io/docs/minesweeper
cp -r ./dist/minesweeper/ ../../akathorn.github.io/docs
cd ../../akathorn.github.io/
git add docs/minesweeper/*.js
git commit -a -m "Update minesweeper app"
git push