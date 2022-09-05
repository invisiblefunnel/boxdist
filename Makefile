default: test

test: install
	python -m unittest tests/**/*.py

install: build
	pip install -e ".[tests]"

build: clean src/boxdist/boxdist.c
	python setup.py sdist bdist_wheel

src/boxdist/boxdist.c:
	cythonize -3 src/boxdist/boxdist.pyx

clean:
	rm -rf build dist *.egg-info boxdist.*.so src/boxdist/boxdist.c
