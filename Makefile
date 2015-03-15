src=README.sec data/SYNTAX.sec data/todo.sec

all: README.md

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

mrproper: clean
	-rm -rf tmp data/help.sec

install:
	ln -s $(pwd)/sectxt.py ~/bin

README.md: README.sec
	sectxt.py --markdown $^ > $@
