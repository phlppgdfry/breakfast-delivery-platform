serve:
	python3 -m demo.server

test:
	python3 -m unittest discover -s tests -v

check: test
	python3 -m compileall -q demo tests
	node --check demo/web/app.js

	node --check demo/web/feature.js

report:
	python3 -m demo.report
