install:
	./build.sh install

install-dev:
	./build.sh install-dev

uninstall:
	./build.sh uninstall

test:
	python3 main.py

release:
	./build.sh release