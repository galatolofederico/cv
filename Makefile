.DEFAULT_GOAL := default

default: cv-eng clean

all: cv-eng cv-eng-sig cv-ita cv-ita-sig clean

cv-eng: init texfile-cv-eng
	xelatex cv
	biber cv
	xelatex cv

cv-ita: init texfile-cv-ita
	xelatex cv_ita
	biber cv_ita
	xelatex cv_ita

cv-eng-sig: init texfile-cv-eng-sig
	xelatex cv_sig
	biber cv_sig
	xelatex cv_sig

cv-ita-sig: init texfile-cv-ita-sig
	xelatex cv_ita_sig
	biber cv_ita_sig
	xelatex cv_ita_sig

texfile-cv-eng:
	python3 generate.py --template template.tex --tex-output cv.tex

texfile-cv-ita:
	python3 generate.py --template template-ita.tex --tex-output cv_ita.tex

texfile-cv-eng-sig:
	python3 generate.py --tex-output cv_sig.tex --signature

texfile-cv-ita-sig:
	python3 generate.py --template template-ita.tex --tex-output cv_ita_sig.tex --signature

init:
ifndef MEJSON
		if [ -d me.json ]; then cd me.json; git pull origin master; else git clone https://github.com/galatolofederico/me.json.git; fi
endif

clean:
	rm -rf cv*.log cv*.out cv*.aux cv*.blg cv*.bbl cv*.bcf cv*.run.xml cv*.tex