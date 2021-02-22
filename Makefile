.DEFAULT_GOAL := default

default: cv clean

all: cv cv_sig clean

cv: init texfile
	xelatex cv
	biber cv
	xelatex cv

cv_sig: init texfile
	xelatex cv_sig
	biber cv_sig
	xelatex cv_sig

texfile:
	python3 generate.py

init:
ifndef MEJSON
		if [ -d me.json ]; then cd me.json; git pull origin master; else git clone https://github.com/galatolofederico/me.json.git; fi
endif

clean:
	rm -rf cv.log cv.out cv.aux cv.blg cv.bbl cv.bcf cv.run.xml cv.tex
	rm -rf cv_sig.log cv_sig.out cv_sig.aux cv_sig.blg cv_sig.bbl cv_sig.bcf cv_sig.run.xml cv_sig.tex
	
