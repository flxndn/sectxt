src=README.sec data/SYNTAX.sec data/todo.sec

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

README.md: README.sec
	sectxt.py --markdown $^ > $@
