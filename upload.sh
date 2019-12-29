#! /bin/sh
cp -pr ../ud-kanbun/conllusvg/conllusvgview.js udkanbun/conllusvgview.js
cp -pr /usr/local/share/udpipe/ud-kanbun.udpipe udkanbun/ud-kanbun.udpipe
rm -f udkanbun/mecab-kanbun/*
( cd $HOME/projects/mecab-kanbun/final_pulleyblank && tar cf - . ) | ( cd udkanbun/mecab-kanbun && tar xvof - )
rm -fr build dist udkanbun.egg-info
python3 setup.py sdist
git status
twine upload --repository pypi dist/*
exit 0
