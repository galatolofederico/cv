.DEFAULT_GOAL := default

default: cv-eng clean

all: cv-eng cv-eng-sig clean

cv-eng: init texfile-cv-eng
	xelatex cv
	biber cv
	xelatex cv

cv-eng-sig: init texfile-cv-eng-sig
	xelatex cv_sig
	biber cv_sig
	xelatex cv_sig

texfile-cv-eng:
	python3 generate.py --tex-output cv.tex

texfile-cv-eng-sig:
	python3 generate.py --tex-output cv_sig.tex --signature

init:
ifndef MEJSON
		if [ -d me.json ]; then cd me.json; git pull origin master; else git clone https://github.com/galatolofederico/me.json.git; fi
endif

clean:
	rm -rf cv*.log cv*.out cv*.aux cv*.blg cv*.bbl cv*.bcf cv*.run.xml cv*.tex