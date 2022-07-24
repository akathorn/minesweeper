pack () {
    echo "Compressing"
    tar -zcvf game.tar.gz game/game.py game/__init__.py
    echo "Moving assets"
    mv game.tar.gz web-app/src/assets/game.tar.gz
}

listen () {
    while inotifywait -e close_write game/game.py; do pack; done
}

if [[ $* == *--listen* ]]
then
    listen
else
    pack
fi