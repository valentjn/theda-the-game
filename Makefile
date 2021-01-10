all:
	if [ -f cards.svg ]; then inkscape cards.svg -o cards.pdf; fi
	inkscape cards.template.svg -o cards.template.pdf
	if [ -f symbols.svg ]; then inkscape symbols.svg -o symbols.pdf; fi
	inkscape symbols.template.svg -o symbols.template.pdf
	lualatex background.tex
	lualatex background.tex
	lualatex backgroundA4.tex
	lualatex backgroundA4.tex
	lualatex can.tex
	lualatex can.tex
	lualatex cardsA4.tex
	lualatex cardsA4.tex
	lualatex instructions.tex
	lualatex instructions.tex
	lualatex instructionsA4.tex
	lualatex instructionsA4.tex
