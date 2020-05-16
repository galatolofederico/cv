.DEFAULT_GOAL := default

default: pdf clean

pdf: init texfile
	xelatex cv
	biber cv
	xelatex cv

texfile:
	python3 generate.py

init:
	if [ -d me.json ]; then cd me.json; git pull origin master; else git clone https://github.com/galatolofederico/me.json.git; fi

clean:
	rm -rf cv.log cv.out cv.aux cv.blg cv.bbl cv.bcf cv.run.xml cv.tex
