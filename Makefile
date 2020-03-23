test: run_tests clean

run_tests:
	python3 test.py

clean:
	rm -rf __pycache__/
	rm -rf output/*.pdf
	rm -rf output/*.gv

load_db:
	python3 ./src/db_loader.py gtfs/mta.zip

draw:
	python3 -m src.gtfs gtfs.py

load_and_draw: load_db draw
