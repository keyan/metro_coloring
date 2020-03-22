test: run_tests clean

run_tests:
	python3 test.py

clean:
	rm -rf __pycache__/
	rm -rf output/*.pdf
	rm -rf output/*.gv
