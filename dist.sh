#!/bin/sh

cd /cv

mkdir -p /dist
make clean
make all

cp -f cv.pdf /dist
cp -f cv_ita.pdf /dist

cp -f cv_sig.pdf /dist
cp -f cv_ita_sig.pdf /dist