SHELL:=/bin/bash
src:=README.sec doc/SYNTAX.sec doc/todo.sec

FORMATS=["html"]="html" \
		["markdown"]="md" \
		["xml"]="xml" \
		["dokuwiki"]="wiki" \
		["wikipedia"]="wikipedia" \
		["article"]="dbk" \
		["latex"]="tex"

all: README.md doc/help.sec

dirs:
	-mkdir tmp doc

doc/help.sec: sectxt.py
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
	-rm doc/help.sec README.md

mrproper: clean
	-rm -rf tmp doc/help.sec

install:
	target=~/bin/sectxt.py; \
	if [ -e $$target ]]; then rm $$target; fi; \
	ln -s $(pwd)/sectxt.py $$target

test:
	declare -A formats=( ${FORMATS} ); \
	for f in $${!formats[@]}; do \
		t=$$(tempfile); \
		sectxt.py --$$f doc/SYNTAX.sec > $$t; \
		if diff $$t doc/test/SYNTAX.$${formats[$$f]}; then \
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
		sectxt.py --$$f doc/SYNTAX.sec > doc/test/SYNTAX.$${formats[$$f]}; \
	done

README.md: README.sec
	sectxt.py --markdown $^ > $@
