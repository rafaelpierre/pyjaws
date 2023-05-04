build:
	rm -rf pyjaws/dist
	pip install build wheel
	python -m build pyjaws --wheel