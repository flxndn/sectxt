SHELL:=/bin/bash
src:=README.sec data/SYNTAX.sec data/todo.sec

FORMATS=["html"]="html" \
		["markdown"]="md" \
		["xml"]="xml" \
		["dokuwiki"]="wiki" \
		["article"]="dbk" \
		["latex"]="tex"

all: README.md data/help.sec

dirs:
	-mkdir tmp data

data/help.sec: sectxt.py
	./sectxt.py -h > $@
	
checkin: aspell
	svn ci
update: 
	svn up
aspell:
	for i in ${src}; \
	do \
		aspell --lang=en -c $$i; \
	done

clean:
	-rm tmp/* *.pyc
	-rm data/help.sec README.md

mrproper: clean
	-rm -rf tmp data/help.sec

install:
	target=~/bin/sectxt.py; \
	if [ -e $$target ]]; then rm $$target; fi; \
	ln -s $(pwd)/sectxt.py $$target

test:
	declare -A formats=( ${FORMATS} ); \
	for f in $${!formats[@]}; do \
		t=$$(tempfile); \
		sectxt.py --$$f data/SYNTAX.sec > $$t; \
		if diff $$t data/test/SYNTAX.$${formats[$$f]}; then \
			echo "$$f OK"; \
		else \
			echo "$$f Error" >&2; \
		fi; \
		rm $$t; \
	done

test_references: 
	declare -A formats=( ${FORMATS} ); \
	for f in $${!formats[@]}; do \
		echo $$f; \
		sectxt.py --$$f data/SYNTAX.sec > data/test/SYNTAX.$${formats[$$f]}; \
	done

README.md: README.sec
	sectxt.py --markdown $^ > $@
