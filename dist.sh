#!/bin/sh

cd /cv

mkdir -p /dist
make all

cp -f cv.pdf /dist
cp -f cv_sig.pdf /dist