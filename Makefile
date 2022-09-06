default: test

test: install
	python -m unittest tests/*.py

install: type-check
	pip install -e ".[tests]"

type-check:
	mypy boxdist

build: clean
	python setup.py build_ext --inplace
	python setup.py sdist bdist_wheel

clean:
	rm -rf build dist *.egg-info *.so boxdist/*.c
